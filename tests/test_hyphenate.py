# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import hyphenator
h=hyphenator.getInstance()
print h.hyphenate("hyphenate")
