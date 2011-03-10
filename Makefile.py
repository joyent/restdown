# -*- coding: utf-8 -*-

import sys
import os
from os.path import join
from glob import glob

from mklib.common import MkError
from mklib import Task, mk
from mklib import sh


class examples(Task):
    """render examples/*.restdown"""
    default = True
    def make(self):
        for path in glob(join(self.dir, "examples", "*", "*.restdown")):
            os.system("bin/restdown %s" % path)

