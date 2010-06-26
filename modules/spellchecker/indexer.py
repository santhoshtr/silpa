# -*- coding: utf-8 -*-
# DictionaryIndex - Creates the directory index for the spellcheck dictionaries
# Copyright 2008-2010
#       Vasudev Kamath <kamathvasudev@gmail.com>
#       Santhosh Thottingal <santhosh.thottingal@gmail.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys
import os
import timeit
import codecs
sys.path.append("../../")
from utils import *

class DictionaryIndex:
    def __init__(self):
        self.fp = None
        self.op = None
        self.dictionary = dict()
        self.offset = 0
        self.path = os.path.join(os.path.dirname(__file__),"dicts")
        self.dictionary_file = None
        self.index_file = None

    def create_index(self,dictfile):
        """
       
       Creates index for a dictionary index file is created in form of 
       dictionary object and creates a file by name dictfile.index with
       contents in following format
       A=1
       B=2000 ....
       (For eg. en_US.index)
       
       @param dictfile : name of the dictionary for which index should be created

        """

        self.dictionary_file = dictfile
        self.index_file = os.path.join(dictfile.split(".")[0] + ".index")


        self.fp = codecs.open(self.dictionary_file,"r",encoding="utf-8")
        self.op = codecs.open(self.index_file,"w",encoding="utf-8")

        # loop untill entire file is not finished
        while True:
            item = self.fp.readline()
            if not item:
                break
            
            # if the alphabet is currently not indexed then index it 
            # with current value of byte offset else increase the offset
            # by the byte length of currently read word till you get 
	    # new alphaet which is not indexed
    
            if len(item)>0 and not self.dictionary.has_key(item[0]):
                self.dictionary[item[0]] = self.offset
            self.offset = self.offset + len(item.encode( "utf-8" ))
                
            
        #print "Index for " + self.dictionary_file + " is created "

        for index in self.dictionary:
           value = self.dictionary.get(index,None)
           if not value == None:
                self.op.write(index + "=%d\n"% value)
    
    
        # Clean up
        self.fp.close()
        self.op.close()


    def load_index(self,dictfile):
        """
            This function reads the index file and loads the content into
            a dictionary object. If file doesn't exist this will create the
            index file and then reads it.
            @param dictfile: Dictionary for which the index file is to be loaded
            returns - dictionary object containing indexing information
        """
    
        self.index_file = os.path.join(self.path,dictfile.split(".")[0] + ".index")
        try:
            self.fp = codecs.open(self.index_file,"r",encoding="utf-8",errors="ignore")
        except IOError:
            silpalogger.info("Could not find the dictionary for %s",dictfile)
            self.create_index(dictfile)
       
        self.fp = codecs.open(self.index_file,"r",encoding="utf-8")
        self.dictionary = {}
        while True:
            text = unicode(self.fp.readline())
            if text:
                line = text.split("=")
                if len(line)==2:
                    index = line[0]
                    value = line[1]
                    self.dictionary[index] = value
            else:
                break

        
        self.fp.close()
        return self.dictionary

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: indexer.py dictionary_path"
        print "Example: indexer.py dicts/en_US.dic"
        sys.exit()
    dictionary_path = sys.argv[1]
    index = DictionaryIndex()
    t1 = timeit.Timer()
    index.create_index(dictionary_path)
    print t1.timeit()
