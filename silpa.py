#!/home/smcweb/bin/python
# -*- coding: utf-8 -*-
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
        action=None
        headers = [('Content-Type', 'text/html')]
        try:
            requesturi = environ['REQUEST_URI']
        except:
            requesturi = None
        #JSON RPC requests
        if requesturi == "/silpa/JSONRPC":
            try:
                content_length= int(environ['CONTENT_LENGTH'])
            except: 
                content_length = 0
            if  content_length > 0 :
                data = environ['wsgi.input'].read(content_length).decode("utf-8")
                start_response('200 OK', headers)
                headers = [('Content-Type', 'application/json')]
                jsonreponse = self._jsonrpc_handler.handleRequest(data)
                return [jsonreponse.encode('utf-8')]
        request=SilpaRequest(environ)
        action = request.get('action')  
        from common.silparesponse import SilpaResponse
        self._response=SilpaResponse()
        if action :
            action=action.replace(" ","_")
            #Check if the action is defined.
            if self._module_manager.find_module(action):
                module_instance =  self._module_manager.getModuleInstance(action)
                if(module_instance):
                    #handleStats()  
                    self._response.setForm(module_instance.get_form())
                    start_response('200 OK', headers)
                    return [self._response.toString().encode('utf-8')]
            #It is a static content request.
            self._response.setContent(getStaticContent(action))
            start_response('200 OK', headers)
            return [self._response.toString().encode('utf-8')]
        else: #No action. Show home page
            self._response.setContent(getStaticContent('home.html'))
            start_response('200 OK', headers)
            return [self._response.toString().encode('utf-8')]

