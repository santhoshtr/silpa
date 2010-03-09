#  Language Detection based on unicode range
# -*- coding: utf-8 -*
#  Copyright © 2008-2010  Santhosh Thottingal <santhosh.thottingal@gmail.com>
#  Released under the GPLV3+ license.
import string

def detect_lang(text):
    """
    Detect the language of the given text using the unicode range.
    This function can take a chunk of text and return a dictionary
    containing word-language key-value pairs.
    """
    words=text.split(" ")
    word_count=len(words)
    word_iter=0
    word=""
    result_dict=dict()
    while word_iter < word_count:
        word=words[word_iter]
        if(word):
            orig_word =  word 
            #remove the punctuations
            for punct in string.punctuation:
                word = word.replace(punct," ")    
            length = len(word)
            index = 0
            # scan left to write, skip any punctuations, the detection stops in the first match itself.
            while index < length:
                letter=word[index]
                if not letter.isalpha():
                    index=index+1   
                    continue
                if ((ord(letter) >= 0x0D00) &  (ord(letter) <=0x0D7F)):
                    result_dict[orig_word]= "ml_IN"
                    break
                if ((ord(letter) >= 0x0980) &  (ord(letter) <= 0x09FF)):
                    result_dict[orig_word]= "bn_IN"
                    break
                if ((ord(letter) >= 0x0900) &  (ord(letter) <= 0x097F)):
                    result_dict[orig_word]= "hi_IN"
                    break
                if ((ord(letter) >=0x0A80) &  (ord(letter) <= 0x0AFF)):
                    result_dict[orig_word]= "gu_IN"
                    break
                if ((ord(letter) >= 0x0A00) &  (ord(letter) <=0x0A7F)):
                    result_dict[orig_word]= "pa_IN"
                    break
                if ((ord(letter) >= 0x0C80) &  (ord(letter) <=0x0CFF)):
                    result_dict[orig_word]= "kn_IN"
                    break
                if ((ord(letter) >= 0x0B00) &  (ord(letter) <= 0x0B7F)):
                    result_dict[orig_word]= "or_IN"
                    break
                if ((ord(letter) >= 0x0B80) &  (ord(letter) <= 0x0BFF)):
                    result_dict[orig_word]= "ta_IN"
                    break
                if ((ord(letter) >= 0x0C00) &  (ord(letter) <= 0x0C7F)):
                    result_dict[orig_word]= "te_IN"
                    break
                if ((letter <= u'z')): #this is fallback case.
                    result_dict[orig_word]= "en_US"
                    break
                index=index+1   
        word_iter=word_iter+1   
    return result_dict
