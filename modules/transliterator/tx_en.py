#! /usr/bin/env python
# -*- coding: utf-8 -*-

def transliterate_xx_en(word, src_lang_code):
	virama=u"്"
	#TODO: how to make this more generic so that more languages can be handled here?
	#idea1: transliterate any langauge to a common language say hindi and the n do conversion?
	#existing transliterate.py can be used?
	#idea2: Have dictionaries for each language like english_xx_dict ?
	#TODO: complete this
	english_ml_dict={u'അ':'a',u'ആ':'a',u'ഇ':'a',u'ഈ':'a',u'ഉ':'a',u'ഊ':'a',u'ഋ':'a',\
			u'എ':'a',u'ഏ':'a',u'ഐ':'a',u'ഒ':'a',u'ഓ':'a',u'ഔ':'a',\
			u'ക':'k',u'ഖ':'kh',u'ഗ':'g',u'ഘ':'gh',u'ങ്ങ':'ng',\
			u'ച':'ch',u'ഛ':'chh',u'ജ':'j',u'ഝ':'jhh',u'ഞ':'nj',\
			u'ട':'t',u'ഠ':'th',u'ഡ':'d',u'ഢ':'dh',u'ണ':'n',\
			u'ത':'th',u'ഥ':'th',u'ദ':'d',u'ധ':'dh',u'ന':'n',\
			u'പ':'p',u'ഫ':'ph',u'ബ':'b',u'ഭ':'bh',u'മ':'m',\
			u'യ':'y',u'ര':'r',u'ല':'l', u'വ':'v', u'റ':'r',\
			u'ശ':'sa',u'ഷ':'sh',u'സ':'s', u'ഹ':'h',u'ള':'l',u'ഴ':'zh',\
			u'ാ':'a',u'ി':'i' ,u'ീ':'ee' ,u'ു':'u',\
			u'ൂ':'uu',u'ൃ':'ri' ,u'െ':'e' ,u'േ':'e',\
			u'ൈ':'ai',u'ൊ':'o' ,u'ോ':'oo' ,u'ൗ':'au'}
	word_length	=len(word)
	index=0
	tx_string=""
	while index<word_length:
		a_vowel=""
		if(index+1<word_length):
			try:
				if(word[index+1]==virama):
					a_vowel=""		
				else:
					if (english_ml_dict[word[index+1]] in ['a','e','i','o','u']):
						a_vowel=""				
					else:	
						a_vowel="a"		
					if (english_ml_dict[word[index]] in ['a','e','i','o','u']):	
						a_vowel=""				
					tx_string=tx_string+ english_ml_dict[word[index]] + a_vowel
			except:		
				tx_string=tx_string+ word[index]
		index=index+1	
	return 	tx_string
def transliterate_en_xx(word, target_lang_code):
	#എന്തു ചെയ്യും?
	return 	word
	
if __name__ == "__main__":
	print transliterate_xx_en (u"കരയുന്നോ പുഴ ചിരിക്കുന്നോ?" , "ml_IN")
