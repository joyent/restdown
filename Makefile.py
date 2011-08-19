# -*- coding: utf-8 -*-

import sys
import os
from os.path import join, dirname, normpath, abspath
from glob import glob
import re
import codecs


from mklib.common import MkError
from mklib import Task, mk
from mklib import sh


class examples(Task):
    """render examples/*.restdown"""
    def make(self):
        pats = ["*.restdown", "*.md", "*.rd"]
        for pat in pats:
            for path in glob(join(self.dir, "examples", "*", pat)):
                os.system("bin/restdown -D mediaroot=media %s" % path)

class cut_a_release(Task):
    """automate the steps for cutting a release"""
    proj_name = "restdown"
    version_py_path = "bin/restdown"
    _changes_parser = re.compile(r'^## restdown (?P<ver>[\d\.abc]+)'
        r'(?P<nyr>\s+\(not yet released\))?'
        r'(?P<body>.*?)(?=^##|\Z)', re.M | re.S)

    def make(self):
        DRY_RUN = False
        version_info = self._get_version_info()
        version = self._version_from_version_info(version_info)

        # Confirm
        if not DRY_RUN:
            answer = query_yes_no("* * *\n"
                "Are you sure you want cut a %s release?\n"
                "This will involved commits and a push." % version,
                default="no")
            print "* * *"
            if answer != "yes":
                self.log.info("user abort")
                return
        self.log.info("cutting a %s release", version)

        # Checks: Ensure there is a section in changes for this version.
        changes_path = join(self.dir, "CHANGES.md")
        changes_txt = changes_txt_before = codecs.open(changes_path, 'r', 'utf-8').read()
        changes_sections = self._changes_parser.findall(changes_txt)
        top_ver = changes_sections[0][0]
        if top_ver != version:
            raise MkError("top section in `CHANGES.md' is for "
                "version %r, expected version %r: aborting"
                % (top_ver, version))
        top_nyr = changes_sections[0][1]
        if not top_nyr:
            answer = query_yes_no("\n* * *\n"
                "The top section in `CHANGES.md' doesn't have the expected\n"
                "'(not yet released)' marker. Has this been released already?",
                default="yes")
            print "* * *"
            if answer != "no":
                self.log.info("abort")
                return
        top_body = changes_sections[0][2]
        if top_body.strip() == "(nothing yet)":
            raise MkError("top section body is `(nothing yet)': it looks like "
                "nothing has been added to this release")

        # Commits to prepare release.
        changes_txt = changes_txt.replace(" (not yet released)", "", 1)
        if not DRY_RUN and changes_txt != changes_txt_before:
            self.log.info("prepare `CHANGES.md' for release")
            f = codecs.open(changes_path, 'w', 'utf-8')
            f.write(changes_txt)
            f.close()
            sh.run('git commit %s -m "prepare for %s release"'
                % (changes_path, version), self.log.debug)

        # Tag version and push.
        curr_tags = set(t for t in _capture_stdout(["git", "tag", "-l"]).split('\n') if t)
        if not DRY_RUN and version not in curr_tags:
            self.log.info("tag the release")
            sh.run('git tag -a "%s" -m "version %s"' % (version, version),
                self.log.debug)
            sh.run('git push --tags', self.log.debug)

        # Commits to prepare for future dev and push.
        next_version_info = self._get_next_version_info(version_info)
        next_version = self._version_from_version_info(next_version_info)
        self.log.info("prepare for future dev (version %s)", next_version)
        marker = "## %s %s\n" % (self.proj_name, version)
        if marker not in changes_txt:
            raise MkError("couldn't find `%s' marker in `%s' "
                "content: can't prep for subsequent dev" % (marker, changes_path))
        changes_txt = changes_txt.replace("## %s %s\n" % (self.proj_name, version),
            "## %s %s (not yet released)\n\n(nothing yet)\n\n## %s %s\n" % (
                self.proj_name, next_version, self.proj_name, version))
        if not DRY_RUN:
            f = codecs.open(changes_path, 'w', 'utf-8')
            f.write(changes_txt)
            f.close()

        ver_path = join(self.dir, normpath(self.version_py_path))
        ver_content = codecs.open(ver_path, 'r', 'utf-8').read()
        next_version_tuple = self._tuple_from_version(next_version)
        marker = "__version_info__ = %r" % (version_info,)
        if marker not in ver_content:
            raise MkError("couldn't find `%s' version marker in `%s' "
                "content: can't prep for subsequent dev" % (marker, ver_path))
        ver_content = ver_content.replace(marker,
            "__version_info__ = %r" % (next_version_tuple,))
        if not DRY_RUN:
            f = codecs.open(ver_path, 'w', 'utf-8')
            f.write(ver_content)
            f.close()

        if not DRY_RUN:
            sh.run('git commit %s %s -m "prep for future dev"' % (
                changes_path, ver_path))
            sh.run('git push')

    def _tuple_from_version(self, version):
        def _intify(s):
            try:
                return int(s)
            except ValueError:
                return s
        return tuple(_intify(b) for b in version.split('.'))

    def _get_next_version_info(self, version_info):
        next = list(version_info[:])
        next[-1] += 1
        return tuple(next)

    def _version_from_version_info(self, version_info):
        v = str(version_info[0])
        state_dot_join = True
        for i in version_info[1:]:
            if state_dot_join:
                try:
                    int(i)
                except ValueError:
                    state_dot_join = False
                else:
                    pass
            if state_dot_join:
                v += "." + str(i)
            else:
                v += str(i)
        return v

    def _get_version_info(self):
        f = codecs.open(self.version_py_path, 'r', 'utf-8')
        content = f.read()
        f.close()
        m = re.search(r'^__version_info__\s*=\s*(.*?)\s*$', content, re.M)
        version_info = eval(m.group(1))
        return version_info


#---- internal support stuff

## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
## end of http://code.activestate.com/recipes/577058/ }}}

def _capture_stdout(argv):
    import subprocess
    p = subprocess.Popen(argv, stdout=subprocess.PIPE)
    return p.communicate()[0]

