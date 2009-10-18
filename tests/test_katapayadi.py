# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import katapayadi
k = katapayadi.getInstance()
print k.get_number(u"സൌഖ്യം")  
print k.get_number(u"ധീരശങ്കരാഭരണം")  
print k.get_number(u"കനഗാംഗി")
print k.get_number(u"കമല")
print k.get_number(u"സ്വച്ഛന്ദം")
print k.get_number(u"ചഡാംശു")
print k.get_number(u"ചണ്ഡാംശുചന്ദ്രാധമകുംഭിപാല")
print k.get_number(u"അനൂനനൂന്നാനനനുന്നനിത്യം")
print k.get_number(u"ആയുരാരോഗ്യസൗഖ്യം")
print k.get_swarasthanas(u"ധീരശങ്കരാഭരണം")  
print k.get_swarasthanas(16)  
