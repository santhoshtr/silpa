# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import calendar
cal=calendar.getInstance()
print cal.panchanga("Thrissur",2010,01,22)
