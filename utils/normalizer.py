# -*- coding: utf-8 -*-
import re
import unicodedata
def normalize(text):
    text = unicodedata.normalize('NFC', text)
    space_re = re.compile('\s+', re.UNICODE)
    text = space_re.sub(' ', text)
    text = normalize_ml (text)
    return text
def normalize_ml (text):
    zwnj_re =  re.compile(u'‍+', re.UNICODE) # remove muliple instances of zwnj
    zwj_re =  re.compile(u'‍+', re.UNICODE) # remove muliple instances of  zwj 
    text = zwj_re.sub(u'‍', text)
    text = zwnj_re.sub(u'‍', text)
    text = text.replace(u"ൺ" , u"ണ്‍")
    text = text.replace(u"ൻ", u"ന്‍")
    text = text.replace(u"ർ", u"ര്‍")
    text = text.replace(u"ൽ", u"ല്‍")
    text = text.replace(u"ൾ", u"ള്‍")
    text = text.replace(u"ൿ", u"ക്‍")
    text = text.replace(u"ന്‍റ", u"ന്റ")
    return text     
#print normalize(u"ഔട്‍‍‍‍‍‍ലുക് മുകളിൽ പകർന്നുതന്ന അറിവിന്‍റെ തേൻകണം ").encode("utf-8")
