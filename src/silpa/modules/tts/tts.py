#!/usr/bin/python
# -*- coding: utf-8 -*-

  ##########################################################################################################################
  # dhvani.py                                                                                                              #
  #                                                                                                                        #
  # Copyright 2011 Vasudev Kamath <kamathvasudev@gmail.com>                                                                #
  #                                                                                                                        #
  # This program is free software; you can redistribute it and/or modify                                                   #
  # it under the terms of the GNU  General Public License as published by                                                  #
  # the Free Software Foundation; either version 3 of the License, or                                                      #
  # (at your option) any later version.                                                                                    #
  #                                                                                                                        #
  # This program is distributed in the hope that it will be useful,                                                        #
  # but WITHOUT ANY WARRANTY; without even the implied warranty of                                                         #
  # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                          #
  # GNU General Public License for more details.                                                                           #
  #                                                                                                                        #
  # You should have received a copy of the GNU General Public License                                                      #
  # along with this program; if not, write to the Free Software                                                            #
  # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,                                                             #
  # MA 02110-1301, USA.                                                                                                    #
  ##########################################################################################################################

import uuid
import os
import codecs
from common import *
from utils import *
from ctypes import c_int,c_short,c_float,c_char_p,c_void_p,byref
from common.silparesponse import SilpaResponse
import dhvani


class TTS(SilpaModule):
    def __init__(self):
        self.dh = dhvani.dhvani_init()
        self.template = os.path.join(os.path.dirname(__file__),"tts.html")
        self.tmp_folder = os.path.join(os.path.dirname(__file__), "tmp")
        self.response = SilpaResponse(self.template)

    def set_request(self,request):
        self.request = request
        self.speech = self.request.get('speech')
        self.text = self.request.get('text')
        self.pitch = self.request.get('pitch')
        self.tempo = self.request.get('tempo')

    def set_start_response(self,start_response):
        self.start_response = start_response

    def get_response(self):
        if self.pitch == None:
            self.pitch ="0"
        if self.tempo == None:
            self.tempo ="0"   
        if self.text != None:
            speech_url =  self.text_to_speech(self.text, self.pitch, self.tempo)
            self.response.response_code = "303 see other" 
            self.response.header  = [('Location', speech_url)]
        return self.response


    def get_mimetype(self):
        if self.format == "ogg":
            return "audio/ogg"
        else:
            return "audio/x-wav"

    def serve(self):
        if self.speech:
            self.start_response('200 OK',[
                    ('Content-disposition','attachment; filename='+self.speech),
                    ('Content-Type',self.get_mimetype())])
            return codecs.open(os.path.join(self.tmp_folder,self.speech)),read()
        
    @ServiceMethod
    def text_to_speech(self,text,pitch=0, tempo=0, format="ogg"):
        self.dh.tempo = c_float(int(tempo))
        self.dh.pitch = c_float(float(pitch))
        if format == "ogg":
            self.dh.output_file_format = dhvani.DHVANI_OGG_FORMAT
        else:
            self.dh.output_file_format = dhvani.DHVANI_WAV_FORMAT
        output_filename= str(uuid.uuid1())[0:5]+"."+format
        speechfile = os.path.join(self.tmp_folder, output_filename)
        self.dh.speech_to_file = 1
        self.dh.output_file_name = c_char_p(speechfile)
        return_type = dhvani.dhvani_say(c_char_p(text.encode("utf-8")),byref(self.dh))
        dhvani.dhvani_close()
        if return_type == dhvani.DHVANI_OK:
            return "modules/tts/tmp/"+output_filename
        else:
            return return_type 

    def get_module_name(self):
        return "Text to speech"
    def get_info(self):
        return "Converts text in Indian languages to speech"    
        
def getInstance():
    return TTS()

       
        
