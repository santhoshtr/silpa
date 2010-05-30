# -*- coding: utf-8 -*-
# Copyright 2009-2010
# Santhosh Thottingal <santhosh.thottingal@gmail.com>
# This code is part of Silpa project.
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
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
from cgi import parse_qs
from Cookie import BaseCookie
import cgi
import re
class SilpaRequest(object):
    
    def __init__(self, environ):
        if environ:
            self._formvalues = self._parse_query(environ)
            self._cookies = self._parse_cookies(environ)
        self._environ=environ
    
    def getCookie(self, key):
        try:
            return self._cookies[key]
        except:
            return None 
        
    def get(self , key) :
        if(self._formvalues.has_key(key)):
            return self._formvalues[key].value  
        return self._environ.get(key,None)
    
    def _parse_query(self, environ) :   
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ,  keep_blank_values=1)
        return form
    
    def body(self): 
        length = int(self._environ.get('CONTENT_LENGTH', '0'))
        fileobj = self._environ['wsgi.input']
        return fileobj.read(length).decode("utf-8")
    
    def _parse_cookies(self, environ)   :
        _QUOTES_RE = re.compile('"(.*)"')
        source=environ.get('HTTP_COOKIE', '')
        vars = {}
        if source:
            cookies = BaseCookie()
            cookies.load(source)
            for name in cookies:
                value = cookies[name].value
                unquote_match = _QUOTES_RE.match(value)
                if unquote_match is not None:
                    value = unquote_match.group(1)
                vars[name] = value
        return vars
