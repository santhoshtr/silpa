# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../src/")
from silpa.modules import tts
tts1=tts.getInstance()
print tts1.text_to_speech(u"പൂങ്കോഴി കൂവിയില്ല")
tts2=tts.getInstance()
print tts2.text_to_speech(u"ഇന്നലെ പഴയ ഫ്രണ്ട് ലൈന്‍ മാസികകള്‍ പരതവെ ഇ എം എസ് ന്റെ ഒരു ലേഖനം കിട്ടി.രാഷ്ട്രീയക്കാരും ക്രിമിനലുകളും തമ്മിലുള്ള അവിഹിത ബന്ധത്തെ")
