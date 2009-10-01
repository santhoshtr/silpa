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
		
		
if __name__ == '__main__':
    unittest.main()

#print sc.suggest(u"തമിഴ്നാട്") 
#print sc.check(u"")
#print sc.suggest(u"അംഗങ്ങളാകുന്നുവ")
#print sc.suggest("calculateq")
#print sc.levenshtein(u"സന്മനസ്", u"സന്തോഷ്")
