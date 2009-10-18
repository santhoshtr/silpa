# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import inexactsearch
search=inexactsearch.getInstance()
print search.compare("help","help")
print search.compare(u"സന്തോസ്",u"സന്തോഷ്")
print search.compare(u"സന്തോഷിന്റെ",u"സന്തോഷ്")
print search.compare(u"ஸந்தௌஷ்",u"സന്തോഷ്")
print search.compare(u"ഝത്തീസ്‌ഖഢ്",u"छत्तीसगढ़")
print search.compare(u"ജതീസ്‌ഖഡ്",u"छत्तीसगढ़")
print search.compare(u"ജതീസ്‌ഖഡ്",u"ജതീസ്ഖഡിലെ")
