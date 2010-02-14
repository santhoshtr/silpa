# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import tts
tts=tts.getInstance()
print tts.text_to_wave("help me please")
