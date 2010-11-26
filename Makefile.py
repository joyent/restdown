# -*- coding: utf-8 -*-

import re
import time
import sys
import codecs
from os.path import expanduser, basename, splitext, dirname, join
from glob import glob

from mklib.common import MkError
from mklib import Task, mk
from mklib import sh

sys.path.insert(0, expanduser("~/tm/python-markdown2/lib"))
import markdown2


class examples(Task):
    """render examples/*.restdown"""
    default = True
    def make(self):
        for path in glob(join(self.dir, "examples", "*.restdown")):
            restdown_path(path)

opts = {
    "extras": {
        "toc": True,
        "markdown-in-html": True,
    }
}


class Restdowner(markdown2.Markdown):
    _skipped_first_h1 = False
    def header_id_from_text(self, text, prefix, n):
        if n == 1 and not self._skipped_first_h1:
            self._skipped_first_h1 = True
        elif n == 1:
            return super(Restdowner, self).header_id_from_text(text, prefix, n)
        elif n == 2:
            # "GET /sshkeys/:id" -> "GET-/sshkeys/:id"
            return text.replace(' ', '-')

    _endpoint_header_re = re.compile(
        r'''^(<h2)( id=".*?"*>)([A-Z]+\s+.*?)(</h2>)$''', re.M)
    _pre_command_block_re = re.compile(r'<pre><code>\$ (.*?)</code></pre>', re.S)
    def postprocess(self, text):
        # Add markup to endpoint h2's for styling.
        text = self._endpoint_header_re.sub(
            r'\1 class="endpoint"\2<span>\3</span>\4', text)
        # Identify shell pre-blocks for styling.
        text = self._pre_command_block_re.sub(
            r'<pre class="shell"><code class="prompt">\1</code></pre>', text)
        return text

    _endpoint_re = re.compile(r'^([A-Z]+)(\s+)(.*?)$')
    def _toc_add_entry(self, level, id, name):
        if level == 2:
            name = self._endpoint_re.sub(
                r'<span class="verb">\1</span>\2<span>\3</span>', name)
        super(Restdowner, self)._toc_add_entry(level, id, name)

def restdown_path(path):
    markdown = codecs.open(path, 'r', 'utf-8').read()
    metadata = {}
    if markdown.startswith("---"):
        _, metastr, markdown = re.compile(r"^---[ \t]*$", re.M).split(
            markdown, 2)
        for line in metastr.strip().splitlines(False):
            line = line.strip()
            if not line:
                continue
            k, v = line.split(':', 1)
            metadata[k.strip()] = v.strip()
    if "title" not in metadata:
        title = ' '.join(s.capitalize()
            for s in splitext(basename(path))[0].split('-'))
        metadata["title"] = title
    html = restdown(metadata, markdown)

    base, ext = splitext(basename(path))
    output_path = join(dirname(path), base + ".html")
    codecs.open(output_path, "w", "utf-8").write(html)
    print("wrote '%s'" % output_path)




def restdown(metadata, markdown):
    """Convert the given metadata and markdown content to restdown HTML.

    @param metadata {dict} Relevant metadata keys are:
            "title"    the HTML document title
        TODO: add more of these for parameterizing things like branding images
    @param markdown {str} The markdown content to convert
    @returns {str} The HTML document (full page)
    """
    html = Restdowner(**opts).convert(markdown)
    metadata["toc_html"] = html.toc_html

    #print html.toc_html
    #print html._toc

    bits = []
    bits.append(u"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="restdown.css">
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
</head>
<body>
    <div id="header">
        <h1>%(title)s Documentation</h1>
    </div>
    <div id="sidebar">
%(toc_html)s
    </div>
    <div id="content">
""" % metadata)
    bits.append(html)
    bits.append(u"""
    </div>
<script type="text/javascript" charset="utf-8">
$(function() {
    var headerHeight = $("#header").height();
    var offsets = [];
    var current = -1;

    function endpoint(scrollDistance) {
        if (scrollDistance < offsets[0]) {
            return -1;
        } else {
            for (var id = offsets.length; id > 0; id--) {
                if (scrollDistance > offsets[id - 1]) {
                    return id - 1;
                    break;
                }
            }
        }
    }

    $("h2.endpoint").each(function(i) {
        offsets.push($(this).offset().top - headerHeight)
    });

    $("#content").append('<h2 class="endpoint fixed" style="display: none"><span>&nbsp;</span></h2>');
    var fixed_h2 = $("h2.fixed");
    var fixed_span = $("h2.fixed span");

    $("#content").scroll(function() {
        var scrollDistance = $("#content").attr('scrollTop');
        var now = endpoint(scrollDistance);

        if (now !== current) {
            $("#sidebar li").removeClass("current");
            current = now;
            if (current < 0) {
                fixed_h2.hide();
            } else if (current >= 0) {
                var heading = $($("h2.endpoint span")[current]).text();
                $("#sidebar a[href|=#" + heading.replace(' ', '-') + "]").parent().addClass("current");
                fixed_span.text(heading);
                fixed_h2.show();
            }
        }
    });
});

</script>
</body>
</html>""")
    return u''.join(bits)
