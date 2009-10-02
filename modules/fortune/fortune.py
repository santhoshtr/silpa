# Fortune
# -*- coding: utf-8 -*-
#
#  Copyright © 2009  Santhosh Thottingal <santhosh.thottingal@gmai.com>
#  Released under the GPLV3+ license

import os,random
from common import *
class Fortune(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'fortune.html')
    
    def fortunes(self,infile,pattern=None):
        """ Yield fortunes as lists of lines """
        quotes = []
        quote = ''
        for line in infile:
            line = line.decode("utf-8")
            if line == "%\n":
                quotes.append(quote)
                quote = ''
                continue
            else:
                quote+=line
        if(pattern!=None):
            for quote in  quotes:
                if(quote.find(pattern) < 0):
                    quotes.remove(quote)     
        return quotes   
        
    @ServiceMethod          
    def fortune(self, database, pattern=None ):
        filename = os.path.join(os.path.dirname(__file__), 'database', database)
        """ Pick a random fortune from a file """
        fortunes_list=self.fortunes(file(filename),pattern)
        chosen=""
        if fortunes_list:
            chosen= random.choice(fortunes_list)
        return "".join(chosen)
    
    def get_module_name(self):
        return "Fortune Cookies"
    def get_info(self):
        return  "Get/Search a random Malayalam quote "
def getInstance():
    return Fortune()    
