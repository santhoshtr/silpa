# -*- coding: utf-8 -*-
import sys
sys.path.append("../src/")
from silpa.modules import payyans
payyan = payyans.getInstance()
#print payyan.ASCII2Unicode(u"hmÀjnI" , "karthika")
#print payyan.Unicode2ASCII(u"വാര്‍ഷിക", "karthika")
#print payyan.Unicode2ASCII(u"ദൈവം", "matweb")
#print payyan.ASCII2Unicode(u"ööalù", "matweb")
#print payyan.Unicode2ASCII(u"ദൈവം", "karthika")
#print payyan.ASCII2Unicode(u"ssZhw", "karthika")
print payyan.Unicode2ASCII(u"അവര്‍ അവനെ", "revathi")
