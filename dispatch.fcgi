#!/home/smcweb/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import traceback
import sys,os
import cgitb
import cgi
sys.path.append(os.path.dirname(__file__))
cgitb.enable(True,os.path.join(os.path.dirname(__file__), "logs"))
from common import *
from silpa import Silpa

def application(environ, start_response):
    silpa = Silpa()
    return silpa.serve(environ, start_response)

if __name__ == '__main__':
    silpa = Silpa()
    WSGIServer(silpa.serve).run()
    
        
