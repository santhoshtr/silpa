#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Unicode Character Details
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# If you find any bugs or have any suggestions email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in
from common import *
from utils import *
import os,sys
import datetime
from sakacalendar import SakaCalendar
class Calendar(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'calendar.html')
        
    @ServiceMethod          
    def date(self, calendar_system="Gregorian"):
        if calendar_system == "Gregorian":
            return dumps([datetime.date.today().year, datetime.date.today().month, datetime.date.today().day] )
        if calendar_system == "Saka"  :
            sakacalendar = SakaCalendar()
            greg= [datetime.date.today().year, datetime.date.today().month, datetime.date.today().day]
            return dumps(sakacalendar.gregorian_to_saka_date(greg))
            
    @ServiceMethod          
    def convert(self, from_calendar_system, to_calendar_system, year, month, day):
        if from_calendar_system == to_calendar_system:
            return dumps([year, month,day])
        sakacalendar = SakaCalendar()
        jd=None
        year = int(year)
        month = int(month)
        day = int(day)
        if  from_calendar_system == "Gregorian":
            jd=sakacalendar.gregorian_to_julian_date(year, month,day)            
        if  from_calendar_system == "Saka":
            jd=sakacalendar.saka_to_julian_date(year, month,day)            
        if to_calendar_system   == "Gregorian":
            return dumps(sakacalendar.julian_date_to_gregorian(jd))
        if to_calendar_system == "Saka":
            return dumps(sakacalendar.gregorian_to_saka_date(sakacalendar.julian_date_to_gregorian(jd)))
        return "Not Implemented " + from_calendar_system + " -> " + to_calendar_system
        
    def get_module_name(self):
        return "Indic Calendar Systems"
    def get_info(self):
        return  "Conversion and look up on Indic Calendars"  
        
def getInstance():
    return Calendar()
