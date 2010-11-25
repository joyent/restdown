
import time
import sys
from os.path import expanduser

from mklib.common import MkError
from mklib import Task, mk
from mklib import sh


class render(Task):
    """render no.de.markdown"""
    default = True
    def make(self):
        sys.path.insert(0, expanduser("~/tm/python-markdown2/lib"))
        import markdown2
        path = "examples/no.de.markdown"
        print "Hi"

