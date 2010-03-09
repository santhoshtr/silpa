# -*- coding: utf-8 -*-
import sys,os
sys.path.append("../../")
from silpa.modules import transliterator
tx=transliterator.getInstance()
print tx.transliterate(u"இலவச,", "ml_IN").encode("utf-8")
print tx.transliterate(u"-സന്ധ്യ", "ta_IN").encode("utf-8")
print tx.transliterate(u" 8 *", "ta_IN").encode("utf-8")
print tx.transliterate(u"ಆಧಾರವಾಗಿರುವ","ml_IN").encode("utf-8")
print tx.transliterate(u"தீபாவளி வாழ்த்துகள்","ml_IN").encode("utf-8")
print tx.transliterate(u"தீபாவளி வாழ்த்துகள்","kn_IN").encode("utf-8")
print tx.transliterate(u"ഔട്‍‍‍‍‍‍ലുക് മുകളിൽ പകർന്നുതന്ന അറിവിന്‍റെ തേൻകണം ","ml_IN").encode("utf-8")
print tx.transliterate(u"translation", "ml_IN").encode("utf-8")
print tx.transliterate(u"ശാരദ സന്ധ്യകള്‍ മരവൂരി ചുറ്റൂം", "ISO15919")
print tx.transliterate(u"ശാരദ സന്ധ്യകള്‍ മരവൂരി ചുറ്റൂം", "IPA")
print tx.transliterate(u"some english text", "IPA")
print tx.transliterate("how was the match?", "hi_IN")
