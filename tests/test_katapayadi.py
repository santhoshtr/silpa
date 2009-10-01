# -*- coding: utf-8 -*-
import sys,os
import unittest
sys.path.append("../../")
from silpa.modules import katapayadi
class TestGuessLangauge(unittest.TestCase):
	def setUp(self):
		self.katapayadi = katapayadi.getInstance()
	def  testKatapayadi(self):
		self.assertEqual(self.katapayadi.get_number(u"ചണ്ഡാംശുചന്ദ്രാധമകുംഭിപാല"),31415926536L)
		self.assertEqual(self.katapayadi.get_number(u"അനൂനനൂന്നാനനനുന്നനിത്യം"),10000000000L)
		self.assertEqual(self.katapayadi.get_number(u"ആയുരാരോഗ്യസൗഖ്യം"),1712210)
	def testSwarasthanas(self):
		self.assertEqual(self.katapayadi.get_swarasthanas(u"ധീരശങ്കരാഭരണം"),u'["Sa","Ri2","Ga3","Ma1","Pa","Da2","Ni3","Sa"]')
if __name__ == '__main__':
    unittest.main()
 
