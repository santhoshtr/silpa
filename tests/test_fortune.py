# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import fortune
f = fortune.getInstance()
print f.fortune('thirukkural',u"உயிர்நிலை")  
print f.fortune('chanakya')  
