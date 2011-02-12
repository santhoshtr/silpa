# -*- coding: utf-8 -*-
import unittest
import sys,os
sys.path.append("../../")
from silpa.modules import guesslanguages

class TestGuessLangauge(unittest.TestCase):

    def setUp(self):
		self.guess_language=guesslanguages.getInstance()

    def testGuessLanguage(self):
        self.assertEqual(self.guess_language.guessLanguage(u"cat"),"English")
        self.assertEqual(self.guess_language.guessLanguage(u"ಪ್ರಸಕ್ತವಾಗಿ"),"Kannada")
        self.assertEqual(self.guess_language.guessLanguage(u"ക്രമീകരണം"),"Malayalam")
        self.assertEqual(self.guess_language.guessLanguage("Reference desk – Serving as virtual librarians, Wikipedia volunteers tackle your questions on a wide range of subjects.")	,"English")
    def testGuessLanguageId(self):
        self.assertEqual(self.guess_language.guessLanguageId(u"ಪ್ರಸಕ್ತವಾಗಿ"),"kn_IN")
        self.assertEqual(self.guess_language.guessLanguageId(u"ക്രമീകരണം"),"ml_IN")
        self.assertEqual(self.guess_language.guessLanguageId("Reference desk – Serving as virtual librarians, Wikipedia volunteers tackle your questions on a wide range of subjects.")	,"en_US")


if __name__ == '__main__':
    unittest.main()


