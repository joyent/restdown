# -*- coding: utf-8 -*-

import re
import time
import sys
import codecs
from os.path import expanduser, basename, splitext

from mklib.common import MkError
from mklib import Task, mk
from mklib import sh


class render(Task):
    """render no.de.markdown"""
    default = True
    def make(self):
        path = "examples/no.de.markdown"
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
            metadata["title"] = splitext(basename(path))[0] + " API"
        html = restdown(metadata, markdown)
        codecs.open("foo.html", "w", "utf-8").write(html)
        self.log.info("wrote 'foo.html'")

opts = {
    "extras": {
        "toc": True,
        "markdown-in-html": True,
    }
}

def restdown(metadata, markdown):
    #TODO: START HERE
    # - "endpoint" styling
    # - "endpoint" JS. Does the new markup and lack of "enpoint fixed" work?
    # - header-ids extra:
    #   - add *which* header level to the "header_id_from_text" callback
    #   - allow that callback to return None to not have an id (empty str
    #     already works for that?)
    #   - override that here to only put header ids for h1, h2
    # - toc
    # - <pre class="req">  How? Hack it?
    sys.path.insert(0, expanduser("~/tm/python-markdown2/lib"))
    import markdown2

    html = markdown2.markdown(markdown, **opts)
    metadata["toc_html"] = html.toc_html

    bits = []
    bits.append(u"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>%(title)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="restdown.css">
</head>
<body>
    <div id="header">
        <h1>%(title)s Documentation</h1>
    </div>
    <div id="sidebar">
        <div class="vertical_divider"></div>
        <ul id="categories">
          <li class="category">
            <h1 class="welcome current"><a href="/">Welcome</a></h1>
          </li>
          <li class="category">
            <ul>
                <li><span class="verb">GET</span><a href="/#GET-/account">/account</a></li>
                <li><span class="verb">PUT</span><a href="/#PUT-/account">/account</a></li>
                <li><span class="verb">POST</span><a href="/#POST-/account">/account</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/sshkeys">/sshkeys</a></li>
                <li><span class="verb">POST</span><a href="/#POST-/sshkeys">/sshkeys</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/sshkeys/:id">/sshkeys/:id</a></li>
                <li><span class="verb">PUT</span><a href="/#PUT-/sshkeys/:id">/sshkeys/:id</a></li>
                <li><span class="verb">DEL</span><a href="/#DELETE-/sshkeys/:id">/sshkeys/:id</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/smartmachines/node">/smartmachines/node</a></li>
                <li><span class="verb">POST</span><a href="/#POST-/smartmachines/node">/smartmachines/node</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/smartmachines/node/:id">/smartmachines/node/:id</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/smartmachines/node/:id/progress">/smartmachines/node/:id/progress</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/smartmachines/node/:id/status">/smartmachines/node/:id/status</a></li>
                <li><span class="verb">GET</span><a href="/#GET-/coupons">/coupons</a></li>
                <li><span class="verb">POST</span><a href="/#POST-/♥">/♥</a></li>
            </ul>
          </li>
        </ul>

        %(toc_html)s
    </div>
    <div id="content">
""" % metadata)
    bits.append(html)
    bits.append(u"""
    </div>
</body>
</html>""")
    return u''.join(bits)
