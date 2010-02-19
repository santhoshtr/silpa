#! /usr/bin/env python
# -*- coding: utf-8 -*-
from utils import *
from PyMeld import Meld

class SilpaResponse:
    def __init__(self):
        xhtml = getTemplate()
        self.page = Meld(xhtml)     
    def toString(self):
        return str(self.page)

    def setForm(self,value):
        if(value):
            self.page.form = value

    def setResult(self,value):
        if(value):
            self.page.result= value 

    def setErrorMessage(self,value):
        if(value):
            self.page.errormessage = value

    def setSuccessMessage(self,value):
        if(value):
            self.page.successmessage = value

    def setContent(self, value):
        if value:
            self.page.content = value           

    def setFooter(self, value):
        if value:
            self.page.footer = value
        
