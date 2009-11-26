# Fortune
# -*- coding: utf-8 -*-
#
#  Copyright © 2009  Santhosh Thottingal <santhosh.thottingal@gmai.com>
#  Released under the GPLV3+ license

import os,random
import codecs 
from common import *

class Fortune(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), 'fortune.html')
    
    def fortunes(self, infile, pattern=None):
        """ Yield fortunes as lists of lines """
        quotes = []
        results = []
        quote = ''
        for line in infile:
            #line = unicode(line)
            if line == "%\n":
                quotes.append(quote)
                quote = ''
            else:
                quote += line 
        if pattern:
            for quote in  quotes:
                if quote.find(pattern) >= 0:
                    results.append(quote)
            return results 
        return quotes   
        
    @ServiceMethod          
    def fortune(self, database, pattern=None ):
        filename = os.path.join(os.path.dirname(__file__), 'database', database)
        fortunes_file = codecs. open(filename,encoding='utf-8', errors='ignore')
        """ Pick a random fortune from a file """
        fortunes_list = self.fortunes(fortunes_file, pattern)
        chosen = ""
        if fortunes_list:
            chosen = random.choice(fortunes_list)
        return "".join(chosen)
    
    def get_module_name(self):
        return "Fortune Cookies"
    def get_info(self):
        return  "Get/Search a random quote "
def getInstance():
    return Fortune()    
