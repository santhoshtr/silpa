#  Spellchecker with language detection
#  coding: utf-8
#
#  Copyright © 2008  Santhosh Thottingal
#  Released under the GPLV3+ license
import string
def detect_lang(text):
    words=text.split(" ")
    word_count=len(words)
    word_iter=0
    word=""
    result_dict=dict()
    while word_iter < word_count:
        word=words[word_iter]
        if(word):
            orig_word =  word 
            for punct in string.punctuation:
                word = word.replace(punct," ")    
            length = len(word)
            index = 0
            while index < length:
                letter=word[index]
                if not letter.isalpha():
                    index=index+1   
                    continue
                if ((letter >= u'ം') &  (letter <=u'൯')):
                    result_dict[orig_word]= "ml_IN"
                    break;
                if ((letter >= u'ঁ') &  (letter <= u'৺')):
                    result_dict[orig_word]= "bn_IN"
                    break
                if ((letter >= u'ँ') &  (letter <= u'ॿ')):
                    result_dict[orig_word]= "hi_IN"
                    break
                if ((letter >=u'ઁ') &  (letter <= u'૱')):
                    result_dict[orig_word]= "gu_IN"
                    break
                if ((letter >= u'ਁ') &  (letter <=u'ੴ')):
                    result_dict[orig_word]= "pa_IN"
                    break
                if ((letter >= u'ಂ') &  (letter <=u'ೲ')):
                    result_dict[orig_word]= "kn_IN"
                    break
                if ((letter >= u'ଁ') &  (letter <= u'ୱ')):
                    result_dict[orig_word]= "or_IN"
                    break
                if ((letter >=u'ஂ') &  (letter <= u'௺')):
                    result_dict[orig_word]= "ta_IN"
                    break
                if ((letter >=u'ఁ') &  (letter <= u'౯')):
                    result_dict[orig_word]= "te_IN"
                    break
                if ((letter <= u'z')):
                    result_dict[orig_word]= "en_US"
                    break
                index=index+1   
        word_iter=word_iter+1   
    return result_dict
