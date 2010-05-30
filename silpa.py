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
import cgitb
import cgi
sys.path.append(os.path.dirname(__file__))
from common import *
from utils import *
from jsonrpc import handleCGI,ServiceHandler
cgitb.enable(True,os.path.join(os.path.dirname(__file__), "logs"))
class Silpa():
    
    def __init__(self):
        self._module_manager = ModuleManager()
        self._response=None
        self._jsonrpc_handler=ServiceHandler(self) 
        
    def serve(self,environ, start_response):
        """
        The method to serve all the requests.
        """
        try:
            request_uri = environ['REQUEST_URI']
            # TODO there should be a better way to handle the below line
            request_uri  = request_uri .replace("/silpa/","") #remove app name from uri . 
        except:
            # To handle the python -m silpa server instances.
            request_uri = environ.get('PATH_INFO', '').lstrip('/')
            
        #JSON RPC requests
        if request_uri == "JSONRPC":
            try:
                content_length = int(environ['CONTENT_LENGTH'])
            except: 
                content_length = 0
            if  content_length > 0 :
                data = environ['wsgi.input'].read(content_length).decode("utf-8")
                start_response('200 OK', [('Content-Type', 'application/json')])
                jsonreponse = self._jsonrpc_handler.handleRequest(data)
                return [jsonreponse.encode('utf-8')]
        request = SilpaRequest(environ)
        if  request_uri == None or request_uri .strip()=='': 
            request_uri = request.get('action')  
            
        from common.silparesponse import SilpaResponse
        self._response=SilpaResponse()
        
        if request_uri :
            #Check if the action is defined.
            if self._module_manager.find_module(request_uri ):
                module_instance =  self._module_manager.getModuleInstance(request_uri )
                if(module_instance):
                    module_instance.set_request(request)
                    
                    #if this is a json request
                    if request.get('json'):
                        jsonreponse = module_instance.get_json_result()
                        start_response('200 OK', [('Content-Type', 'application/json')])
                        return [jsonreponse.encode('utf-8')]
                        
                    #normal request for the page, may contain request parameters(GET)    
                    self._response.set_form(module_instance.get_form())
                    self._response.set_result(module_instance.get_result())
                    start_response('200 OK', [('Content-Type', 'text/html')])
                    return [self._response.toString().encode('utf-8')]
                    
            #It is a static content request.
            # Content type depends on the mimetype
            start_response('200 OK', [('Content-Type', getMimetype(request_uri))])
            if request_uri .endswith(".html"):
                # HTML pages need to be embedded inside the content area
                self._response.set_content(getStaticContent("doc/"+request_uri))
                return [self._response.toString().encode('utf-8')]
            else: 
                # Images, css, javascript etc..
                return [getStaticContent(request_uri)]
                
        else: #No action. Show home page
            self._response.set_content(getStaticContent('doc/index.html'))
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [self._response.toString().encode('utf-8')]

