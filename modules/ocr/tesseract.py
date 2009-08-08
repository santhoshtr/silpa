#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys  
import codecs  
import os  
from common import *
class Tesseract(SilpaModule):

	def __init__(self):
		self.input_filename =""
				
	def ocr(self):
		result = ""
		return result
	def process(self,form):
		response = """
		<h2>Tesseract Indic OCR system</h2></hr>
		<p>Upload the .tiff image here.		
		</p>
		<form action="" method="post">
			<input type="file" name="image_file" > 
			<input  type="submit" id="ocr" value="ocr"  name="action" />
			<input  type="submit" id="ocr" value="Submit"  style="width:12em;"/>
		</form>
		"""
		if(form.has_key('image_file')):
			image_file_name = form['image_file'].value	.decode('utf-8')
			response=response  +  image_file_name
		return response
	def get_module_name(self):
		return "Tesseract Indic OCR"
	def get_info(self):
		return 	"Tesseract Indic optical character recognition."	
		
def getInstance():
	return Tesseract()
