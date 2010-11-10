#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys
import re
import os
from common import *
from utils import *
import cairo
import uuid
import urllib
import pango
import pangocairo
from wiki2pdf  import Wikiparser
from modules.hyphenator import hyphenator

class Render(SilpaModule):
    def __init__(self):
        self.template=os.path.join(os.path.dirname(__file__), "render.html")

    def set_request(self,request):
        self.request=request
        self.image = self.request.get('image')
        self.pdf = self.request.get('pdf')
        self.file_type= self.request.get('type')
        self.wiki_url= self.request.get('wiki')

        
    def is_self_serve(self) :       
        if self.image or self.pdf or self.wiki_url:
            return True
        else:
            return False

    def get_mimetype(self):
        if self.image:
            return "image/"+ self.file_type
        if self.pdf or self.wiki_url:    
            return "application/pdf"

    def serve(self):
        """
        Provide the css for the given font. CSS will differ for IE and Other browsers
        """
        
        if self.image:
            return codecs.open(os.path.join(os.path.dirname(__file__),"tmp",self.image)).read()
        else:    
            if self.wiki_url:
				self.pdf = self.wiki2pdf(self.wiki_url).replace("?pdf=", "")
            return codecs.open(os.path.join(os.path.dirname(__file__), "tmp",self.pdf)).read()

    @ServiceMethod  
    def wiki2pdf(self, url):
        filename =  str(uuid.uuid1())[0:5] +".pdf"
        parser = Wikiparser(url,filename) #"http://ml.wikipedia.org/wiki/Computer"
        parser.parse()
        return ("?pdf="+filename)
        
    @ServiceMethod  
    def render_text(self, text,file_type='png', width=600, height=100):
        surface = None
        filename = str(uuid.uuid1())[0:5]+"."+file_type
        outputfile = os.path.join(os.path.dirname(__file__),"tmp",filename )
        if file_type == 'png':
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        else:
            if file_type == 'svg':
                surface = cairo.SVGSurface(outputfile,int(width),int(height))
            elif file_type == 'pdf':
                surface = cairo.PDFSurface(outputfile,int(width),int(height))
                
        context = cairo.Context(surface)
        text = hyphenator.getInstance().hyphenate(text,u'\u00AD')
        width  = int(width)
        font_size = 10
        position_x = int(width)*0.1
        position_y = int(width)*0.1
        context.set_source_rgba (0.0, 0.0, 0.0, 1.0)
        pc = pangocairo.CairoContext(context)
        paragraph_layout = pc.create_layout()
        paragraph_font_description = pango.FontDescription()
        paragraph_font_description.set_family("Sans")
        paragraph_font_description.set_size((int)(font_size * pango.SCALE))
        paragraph_layout.set_font_description(paragraph_font_description)
        paragraph_layout.set_width((int)((width - 2*width*0.1) * pango.SCALE))
        paragraph_layout.set_justify(True)
        paragraph_layout.set_text(text+"\n")
        context.move_to(width*0.1,width*0.1)
        pango_layout_iter = paragraph_layout.get_iter();
        itr_has_next_line=True
        while not pango_layout_iter.at_last_line():
            first_line = True
            context.move_to(width*0.1, position_y)
            while not pango_layout_iter.at_last_line() :
                ink_rect, logical_rect = pango_layout_iter.get_line_extents()
                line = pango_layout_iter.get_line_readonly()
                has_next_line=pango_layout_iter.next_line()
                # Decrease paragraph spacing
                if  ink_rect[2] == 0 : #It is para break
                    dy = font_size / 2
                    position_y += dy
                    if not first_line:
                        self.context.rel_move_to(0, dy)
                else:
                    xstart = 1.0 * logical_rect[0] / pango.SCALE
                    context.rel_move_to(xstart, 0)
                    pc.show_layout_line( line)
                    line_height = (int)(logical_rect[3] / pango.SCALE)
                    context.rel_move_to(-xstart, line_height )
                    position_y += line_height 
            first_line = False
            
        if file_type == 'png':
            surface.write_to_png(outputfile)
        else:
            context.show_page()

        return "?image="+filename+"&type="+file_type

        
    def get_module_name(self):
        return "Script Renderer"
        
    def get_info(self):
        return  "Provides rendered images for Complex scripts"    
        
def getInstance():
    return Render()


