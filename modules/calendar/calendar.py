#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Calendar Program
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
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
from astral import Astral
class Calendar(SilpaModule):
    WEEKDAYS =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'calendar.html')
        self.astral =Astral()
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
    @ServiceMethod
    def panchanga(self, city_name, year,month,day):
		
        date  = datetime.date(int(year), int(month), int(day))
        calendar_details={}
        self.astral.solar_depression = 'civil'
        city = self.astral[city_name]
        calendar_details['Day of the week'] = self.WEEKDAYS[date.isoweekday()]
        calendar_details['City Name'] = city_name
        calendar_details['City Country'] = city.country
        print('Information for %s/%s\n' % (city_name, city.country))
        timezone = city.timezone
        print('Timezone: %s' % timezone)
        calendar_details['Timezone'] =  timezone
        calendar_details['Latitude'] =  city.latitude
        calendar_details['Longitude'] =  city.longitude
        print('Latitude: %.02f; Longitude: %.02f\n' % \
            (city.latitude, city.longitude))
        sun = city.sun(date=date, local=True)
        calendar_details['Dawn'] = str(sun['dawn'])
        calendar_details['Sunrise'] = str(sun['sunrise'])
        calendar_details['Noon'] = str(sun['noon'])
        calendar_details['Sunset'] = str(sun['sunset'])
        calendar_details['Dusk'] = str(sun['dusk'])
        print('Dawn:    %s' % str(sun['dawn']))
        print('Sunrise: %s' % str(sun['sunrise']))
        print('Noon:    %s' % str(sun['noon']))
        print('Sunset:  %s' % str(sun['sunset']))
        print('Dusk:    %s' % str(sun['dusk']))
        rahukaalam = city.rahukaalam(date=date, local=True)
        gulikakaalam = city.gulikakaalam(date=date, local=True)
        yamakandakaalam = city.yamakandakaalam(date=date, local=True)
        calendar_details['Rahukaalam'] = "from " + str(rahukaalam['start']) + " to " +   str(rahukaalam['end'])
        calendar_details['Gulikakaalam'] = "from " + str(gulikakaalam['start']) + " to " +   str(gulikakaalam['end'])
        calendar_details['Yamakandakaalam'] = "from " + str(yamakandakaalam['start']) + " to " +   str(yamakandakaalam['end'])
        print('Rahukaalam:    %s' % "from " + str(rahukaalam['start']) + " to " +   str(rahukaalam['end']))
        print('Gulikakaalam:    %s' %  "from " + str(gulikakaalam['start']) + " to " +   str(gulikakaalam['end']))
        print('Yamakandakaalam:    %s' % "from " + str(yamakandakaalam['start']) + " to " +   str(yamakandakaalam['end']))
        calendar_details['Kollavarsham(Malayalam Calendar)'] = "Not implemented now"
        calendar_details['Tamil Calendar'] = "Not implemented now"
        calendar_details['Bengali Calendar'] = "Not implemented now"
        sakacalendar = SakaCalendar()
        jd=sakacalendar.gregorian_to_julian_date(int(year), int(month),int(day) )           
        calendar_details['Saka Calendar'] = sakacalendar.gregorian_to_saka_date(sakacalendar.julian_date_to_gregorian(jd))
        calendar_details['Oriya Calendar'] = "Not implemented now"
        calendar_details['Nakshathra'] = "Not implemented now"
        calendar_details['Thidhi'] = "Not implemented now"
        
        return dumps(calendar_details)
    def get_module_name(self):
        return "Indic Calendar Systems"
    def get_info(self):
        return  "Conversion and look up on Indic Calendars"  
        
def getInstance():
    return Calendar()
