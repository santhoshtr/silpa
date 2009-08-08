# -*- coding: utf-8 -*-
from common import *
response=SilpaResponse()
response.setBreadcrumb("TestBreadCrumb")
response.setForm("TestContent")
response.setErrorMessage("TestError")	
response.setSuccessMessage("TestSuccess")		
print response
