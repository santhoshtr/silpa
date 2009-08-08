# -*- coding: utf-8 -*-
from jsonrpc import ServiceProxy
s = ServiceProxy("http://smc.org.in/silpadev/services.py")
print s.system.listMethods()
print s.modules.Transliterator.transliterate(u"ശ്രീ ഗ്നു ഈ കമ്പ്യൂട്ടറിന്റെ ഐശ്വര്യം", "hi_IN")
