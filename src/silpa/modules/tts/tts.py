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
from ctypes import CDLL
from ctypes import Structure,CFUNCTYPE,POINTER,byref
from ctypes import c_int,c_short,c_float,c_char_p,c_void_p
from common import *
from utils import *
from common.silparesponse import SilpaResponse

dhvani = CDLL("/usr/local/lib/libdhvani.so.0")


# Define required enums

# dhvani_ERROR enum
(DHVANI_OK,DHVANI_INTERNAL_ERROR) = (0,-1)

# dhvani_output_file_format enum
(DHVANI_OGG_FORMAT,DHVANI_WAV_FORMAT) = (0,1)

# dhvani_Languages enum
(HINDI,MALAYALAM,TAMIL,KANNADA,
 ORIYA,PANJABI,GUJARATI,TELUGU,
 BENGALAI,MARATHI,PASHTO) = (1,2,3,4,5,6,7,8,9,10,11)

# Define call back types
t_dhvani_synth_callback = CFUNCTYPE(c_int,c_int)
t_dhvani_audio_callback = CFUNCTYPE(c_int,POINTER(c_short))

# Unused structure to match original implementation
class dhvani_VOICE(Structure):
    pass

# dhvani_option structure mapping class
class dhvani_options(Structure):
    _fields_ = [("voice",POINTER(dhvani_VOICE)),
                ("pitch",c_float),
                ("tempo",c_float),
                ("rate",c_int),
                ("language",c_int),
                ("output_file_format",c_int),
                ("isPhonetic",c_int),
                ("speech_to_file",c_int),
                ("output_file_name",c_char_p),
                ("synth_callback_fn",POINTER(t_dhvani_synth_callback)),
                ("audio_callback_fn",POINTER(t_dhvani_audio_callback))]


# Define dhvani speech function
dhvani_say = dhvani.dhvani_say
dhvani_say.restype = c_int
dhvani_say.argtypes = [c_char_p,POINTER(dhvani_options)]

# dhvani_speak_file function
dhvani_speak_file = dhvani.dhvani_speak_file
dhvani_speak_file.restype = c_int
dhvani_speak_file.argtypes = [c_void_p,POINTER(dhvani_options)]

# fdopen function not related to dhvani but a C library function
# in stdio.h this is used to
fileopen = dhvani.fdopen
fileopen.restype = c_void_p
fileopen.argtypes = [c_int,c_char_p]

def dhvani_init():
    option = dhvani_options()
    option.language = -1
    option.isPhonetic = 0
    option.speech_to_file = 0
    option.pitch = 0.0
    option.tempo = 0
    option.rate = 16000
    option.synth_callback_fn = None
    option.audio_callback_fn = None
    dhvani.start_synthesizer()
    return option
    
temp_input_file_name = os.path.join("/tmp","tmpInFile")

class TTS(SilpaModule):
    def __init__(self):
        self.rate = 16000
        self.pitch = 0
        self.format = "wav"
        self.option = dhvani_init()
        self.template = os.path.join(os.path.dirname(__file__),"tts.html")
        self.tmp_folder = os.path.join(os.path.dirname(__file__), "tmp")
        self.response = SilpaResponse(self.template)

    def set_request(self,request):
        self.request = request
        self.speech = self.request.get('speech')
        self.text = self.request.get('text')

    def set_start_response(self,start_response):
        self.start_response = start_response

    def is_self_serve(self):
        if self.speech or self.text:
            return True
        else:
            return False

    def get_mimetype(self):
        if self.format == "ogg":
            return "audio/ogg"
        else:
            return "audio/x-wav"

    def serve(self):
        if self.speech:
            self.start_response('200 OK',[
                    ('Content-disposition','attachment; filename='+self.speech),
                    ('Content-Type',self.get_mimetype()),
                    ('Access-Control-Allow-Origin','*')])
            return codecs.open(os.path.join(self.tmp_folder,self.speech)),read()
        
    @ServiceMethod
    def text_to_speech(self,text,pitch=0,speed=16000, format="ogg"):
        self.rate = speed
        self.pitch = pitch
        self.output_format = format

        self.option.rate = c_int(int(self.rate))
        self.option.pitch = c_float(float(self.pitch))

        fp = open(temp_input_file_name,"w")
        fp.write(text)
        fp.close()

        return self._file_to_speech()

    def _file_to_speech(self):
        self.option.rate = c_int(int(self.rate))
        self.option.pitch = c_float(float(self.pitch))

        if self.output_format == "ogg":
            self.option.output_file_format = DHVANI_OGG_FORMAT
        else:
            self.option.output_file_format = DHVANI_WAV_FORMAT

        output_filename= str(uuid.uuid1())[0:5]+"."+self.output_format
        speechfile = os.path.join(self.tmp_folder, output_filename)
        self.option.speech_to_file = 1

        self.option.output_file_name = c_char_p(speechfile)

        # Open the file (not necessary for using codecs lib)
        fp = codecs.open(temp_input_file_name,encoding="utf-8",buffering=0)

        # Now give the file descriptor to fdopen function
        # and get back a FILE* pointer for dhvani_speak_file
        file_pointer = fileopen(fp.fileno(),c_char_p("r"))
        return_type = dhvani_speak_file(c_void_p(file_pointer),byref(self.option))
        fp.close()

        if return_type == DHVANI_OK:
            return "modules/tts/tmp/"+output_filename
        else:
            return 

    def get_module_name(self):
        return "Text to speech"
    def get_info(self):
        return  "Converts text in Indian languages to speech"    
        
def getInstance():
    return TTS()

if __name__ == "__main__":
    d = Dhvani()
    print d._file_to_speech("input.txt")
    text = codecs.open("input.txt",encoding="utf-8").read()
    # print d.text_to_speech(u"ನಮಸ್ಕಾರ ನನ್ನ ಹೆಸರು ವಾಸುದೇವ್".encode("utf-8"),format="ogg")
    # print d.text_to_speech(text.encode("utf-8"),format="ogg")
    
    

        
        
