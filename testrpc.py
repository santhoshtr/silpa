# -*- coding: utf-8 -*-
from jsonrpc import ServiceProxy
s = ServiceProxy("http://smc.org.in/silpa/JSONRPC")
print s.system.listMethods()
print s.modules.InexactSearch.compare("help","help")
