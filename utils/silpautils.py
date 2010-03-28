#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Language Detection based on unicode range
# Copyright 2008 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import codecs
import mimetypes
import os
def getTemplate():
    return open(os.path.dirname(__file__)+"/../"+getTemplateName()).read()

def getTemplateName():
    return loadConfiguration()["SILPA_TEMPLATE"]    

def getCopyrightInfo():
    return loadConfiguration()["SILPA_SITE_COPYRIGHT"]      
    
def getRootFolder():
    #return loadConfiguration()["SILPA_ROOT_FOLDER"]      
    return os.path.dirname(__file__)+ "/../" 

def getModulesList():
    conf_dict=loadConfiguration()
    action_dict={}
    for item in conf_dict   :
        if(item.startswith("SILPA_ACTION.")):
            action_dict[item.replace("SILPA_ACTION.","")] = conf_dict[item]
    return  action_dict 

def getStaticContent(page):
    try:
        return codecs.open(getRootFolder() + "/" + page).read()#, encoding='utf-8', errors='ignore'
    except:
        return "Oops! Requested resource not found!"
    
def loadConfiguration():
    conf_dict={}
    conffile = codecs. open(os.path.dirname(__file__)+"/../silpa.conf",encoding='utf-8', errors='ignore')
    while 1:
        text = unicode( conffile.readline())
        if text == "":
              break
        line = text.split("#")[0].strip()
        if(line == ""):
              continue 
        try:      
            lhs = line.split("=")[0].strip()
            rhs = line.split("=")[1].strip()
            conf_dict[lhs] = rhs
        except:
            pass    
    return conf_dict

def getMimetype(filename):
    type, encoding = mimetypes.guess_type(filename)
    # We'll ignore encoding, even though we shouldn't really
    return type or 'application/octet-stream'

