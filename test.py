# -*- coding: utf-8 -*-
import sys
#sys.path.append("../")
from common import *
def import_module(name):
    parts = name.split(".")
    try:
        obj= sys.modules[name]
        print dir(obj)
    except KeyError:
        obj  = __import__(name)
    if(len(parts)>1):   
        for part in parts[1:]:
            try:
                obj = getattr(obj,part)
            except:
                pass    
    return obj
import_module("modules.transliterator")
import_module("modules.transliterator")
#mm = ModuleManager()
#print mm.getModuleInstance("Transliterate")

