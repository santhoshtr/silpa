#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
class SilpaModule:
	def __init__(self):
		self.template=None
	def get_errormessage(self):
		return None
	def get_successmessage(self):
		return None
	def get_module_name(self):
		return "Untitled Silpa Module"
	def get_info(self):
		return 	"Module description"
	def process(self,object):
		return 	"Not Implemented"
	def get_form(self,templatefile='template.html'):
		return open(self.template).read()

def ServiceMethod(fn):
	fn.IsServiceMethod = True
	return fn
