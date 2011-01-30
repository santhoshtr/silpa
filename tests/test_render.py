# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../src/")
from silpa.modules import render
render=render.getInstance()
#print render.render_image("help me please", "svg", 100,100)
print render.render_text("help me please", "png", 0 ,0)
print render.render_text("help", "png", 0 ,0)
print render.render_text(u"സന്തോഷ്", "png", 0 ,0)
print render.render_text(u"എന്‍ഡോസള്‍ഫാന്‍ നിരോധിക്കണോ വേണ്ടയോ എന്ന് തീരുമാനിക്കാന്‍ ജനീവയില്‍ ചേര്‍ന്ന സ്റോക്ക്ഹോം കണ്‍വെന്ഷന് ഇന്ത്യ വിട്ടിരിക്കുന്നത് എന്‍ഡോസള്‍ഫാന്‍ നിര്‍മ്മാണ കമ്പനിയുടെ എം.ഡി യെ !!! ", "png")
