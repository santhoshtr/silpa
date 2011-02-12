# -*- coding: utf-8 -*-
import random
import unittest
import sys,os
sys.path.append("../../")
from silpa.modules import spellchecker

class TestSpellchecker(unittest.TestCase):
	def setUp(self):
		self.spellchecker=spellchecker.getInstance()
	
	def testLevenshtein(self):
		self.assertEqual(self.spellchecker.levenshtein("hello","helol"), 2)
		self.assertEqual(self.spellchecker.levenshtein("hello","hell0"), 1)
		self.assertEqual(self.spellchecker.levenshtein(u"സന്മനസ്", u"സന്തോഷ്"),3)

	def testSpellcheck(self):
		self.assertEqual(self.spellchecker.check(u"അംഗങ്ങളാകുന്നു"), True)
		self.assertEqual(self.spellchecker.check(u"അവന്‍"), True)
		self.assertEqual(self.spellchecker.check(u"অংসফলক"), True)
		self.assertEqual(self.spellchecker.check(u"അംഗങ്ങളാകുന്നുവ"), False)
	def testSuggestions(self):
		self.assertEqual(self.spellchecker.suggest("calculateq"), u'["calculate","calculated","calculates","calculator"]')
	def testCheckBatch(self):
		self.assertEqual(self.spellchecker.check_batch(u"മോങ്ങാനിരുന്ന നായുടെ തലയില്‍ തേങ്ങാ വീണു."),[])
		
		
if __name__ == '__main__':
    #unittest.main()
    sc = spellchecker.getInstance()
    print sc.check(u"തമിഴ്നാട്") 
    print sc.check(u"തമിഴ്‌നാട്") 
    print sc.suggest(u"തമിഴ്നാട്")
    print sc.suggest("sugest")
    print sc.suggest("suggestwhat")
    print sc.suggest(u"കൂടിയോകൂടിയോ")
    print sc.check(u"ലഭിക്കാവുന്ന")
    print sc.check(u"കൂടിയോ")
#print sc.check(u"")
#print sc.suggest(u"അംഗങ്ങളാകുന്നുവ")
#print sc.suggest("calculateq")
#print sc.levenshtein(u"സന്മനസ്", u"സന്തോഷ്")
