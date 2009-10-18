# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import spellchecker
sc=spellchecker.getInstance()
print sc.levenshtein("hello","helol")
print sc.levenshtein("hello","hell0")
print sc.check(u"അംഗങ്ങളാകുന്നു")
print sc.check(u"അവന്‍")
print sc.check(u"অংসফলক")
print sc.suggest(u"തമിഴ്നാട്") 
print sc.check(u"അംഗങ്ങളാകുന്നുവ")
print sc.suggest(u"അംഗങ്ങളാകുന്നുവ")
print sc.suggest("calculateq")
print sc.levenshtein(u"സന്മനസ്", u"സന്തോഷ്")
