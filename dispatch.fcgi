#!/home/smcweb/bin/python
# -*- coding: utf-8 -*-
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
    
        
