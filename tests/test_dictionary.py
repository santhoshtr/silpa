# -*- coding: utf-8 -*-
import random
import unittest
import sys,os
sys.path.append("../../")
from silpa.modules import dictionary

class TestDictionary(unittest.TestCase):

    def setUp(self):
		self.dictionary=dictionary.getInstance()

    def testEnglishHindi(self):
        self.assertEqual(dictionary.getdef("help","freedict-eng-hin"), "")


if __name__ == '__main__':
    unittest.main()


