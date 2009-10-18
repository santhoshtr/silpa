# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import dictionary
dictionary=dictionary.getInstance()
print dictionary.getdef("help","freedict-eng-hin")
