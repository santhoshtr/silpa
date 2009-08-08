#!/home/smcweb/bin/python
# -*- coding: utf-8 -*-
from common import *
from utils import *
from jsonrpc import handleCGI,ServiceHandler
import traceback
import cgitb
import cgi
cgitb.enable(True, "logs/")
class Silpa():
	def __init__(self):
		self._module_manager = ModuleManager()
		self._response=SilpaResponse()
	def index(self, form):
		action=None
		if(form.has_key('action')):
			action=form['action'].value	
		if(action):
			action=action.replace(" ","_")
			#Check if the action is defined.
			if self._module_manager.find_module(action):
				module_instance =  self._module_manager.getModuleInstance(action)
				if(module_instance):
					handleStats()	
					self._response.setForm(module_instance.get_form())
					return self._response.toString()
			#JSON-RPC service		
			if action == 'JSONRPC':
				handleCGI()
				return 
			#It is a static content request.
			self._response.setContent(getStaticContent(action))
			return self._response.toString()
		else: #No action. Show home page
			self._response.setContent(getStaticContent('home.html'))
			return self._response.toString()				
if __name__ == '__main__':
	silpa = Silpa()
	response = silpa.index(cgi.FieldStorage())
	#In case of JSON RPC calls the response will be send by the RPC handler
	if response :
		print response.encode('utf-8')
		
