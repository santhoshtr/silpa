# -*- coding: utf-8 -*-
import sys
sys.path.append("../src/")
from silpa.modules import syllabalizer
s = syllabalizer.getInstance()
print s.syllabalize(u"കീഴടങ്ങിയിരിപ്പിന്‍")
