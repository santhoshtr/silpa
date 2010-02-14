# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import stemmer
tx=stemmer.getInstance()
print tx.stem(u"ഇല്ലെങ്കില്‍")
