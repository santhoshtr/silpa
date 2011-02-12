#!/home/smcweb/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import traceback
import sys
import os
import datetime
import cgitb
import cgi
sys.path.append(os.path.dirname(__file__))
from common import *
from utils import *
from jsonrpc import ServiceHandler
from common.silparesponse import SilpaResponse

class Silpa():
    
    def __init__(self):
        self._module_manager = ModuleManager()
        self._response=None
        self._jsonrpc_handler=ServiceHandler(self) 
        
    def serve(self,environ, start_response):
        """
        The method to serve all the requests.
        """
        request = SilpaRequest(environ)
        request_uri = environ.get('PATH_INFO', '').lstrip('/')
        
        #JSON RPC requests
        if request_uri == "JSONRPC":
                data = request.get_body()
                start_response('200 OK', [('Content-Type', 'application/json')])
                jsonreponse = self._jsonrpc_handler.handleRequest(data)
                return [jsonreponse.encode('utf-8')]
          
        
        
        #Check if the action is defined.
        if self._module_manager.find_module(request_uri ):
            module_instance =  self._module_manager.get_module_instance(request_uri )
            if(module_instance):
                module_instance.set_request(request)
                module_instance.set_start_response(start_response)
                
                #if this is a json request
                if request.get('json'):
                    jsonreponse = module_instance.get_json_result()
                    start_response('200 OK', [('Content-Type', 'application/json')])
                    return [jsonreponse.encode('utf-8')]
                    
                response = module_instance.get_response()
                start_response(response.response_code, response.header)
                return [str(response.content).encode('utf-8')]
        
        response=SilpaResponse()
        if(request_uri == "index.html" or request_uri == ""):
            start_response('200 OK', [('Content-Type', 'text/html')])
            response.content.content = get_index_page()
        else:
            response.content.content ='Requested URL not found.'
            start_response('404 Not found', [('Content-Type', 'text/html')])
        return [str(response.content).encode('utf-8')]

