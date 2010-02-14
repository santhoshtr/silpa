# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
from jsonrpc import ServiceProxy
s = ServiceProxy("http://localhost/silpa/JSONRPC")
print s.system.listMethods()
#print s.modules.InexactSearch.compare("help","help")
print s.modules.Katapayadi.get_swarasthanas("12")
print s.modules.Calendar.convert("Gregorian","Saka", "1992","12","12")
