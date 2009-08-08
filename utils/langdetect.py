#  Spellchecker with language detection
#  coding: utf-8
#
#  Copyright © 2008  Santhosh Thottingal
#  Released under the GPLV3+ license

def detect_lang(text):
	words=text.split(" ")
	word_count=len(words)
	word_iter=0
	word=""
	result_dict=dict()
	while word_iter < word_count:
		word=words[word_iter]
		if(word):
			length = len(word)
			index = 0
			while index < length:
				letter=word[index]
				if not letter.isalpha():
					index=index+1	
					continue
				if ((letter >= u'ം') &  (letter <=u'൯')):
					result_dict[word]= "ml_IN"
					break;
				if ((letter >= u'ঁ') &  (letter <= u'৺')):
					result_dict[word]= "bn_IN"
					break
				if ((letter >= u'ँ') &  (letter <= u'ॿ')):
					result_dict[word]= "hi_IN"
					break
				if ((letter >=u'ઁ') &  (letter <= u'૱')):
					result_dict[word]= "gu_IN"
					break
				if ((letter >= u'ਁ') &  (letter <=u'ੴ')):
					result_dict[word]= "pa_IN"
					break
				if ((letter >= u'ಂ') &  (letter <=u'ೲ')):
					result_dict[word]= "kn_IN"
					break
				if ((letter >= u'ଁ') &  (letter <= u'ୱ')):
					result_dict[word]= "or_IN"
					break
				if ((letter >=u'ஂ') &  (letter <= u'௺')):
					result_dict[word]= "ta_IN"
					break
				if ((letter >=u'ఁ') &  (letter <= u'౯')):
					result_dict[word]= "te_IN"
					break
				if ((letter <= u'z')):
					result_dict[word]= "en_US"
					break
				index=index+1	
		word_iter=word_iter+1	
	return result_dict
