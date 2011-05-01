import unittest
import sys
sys.path.append("../src/")
from silpa.modules import dictionary

class TestWiktionary(unittest.TestCase):
    def setUp(self):
        self.dictionary = dictionary.getInstance()

    def testEnglishHindi(self):
        self.dictionary.get_response()
        print "Testing English to Hindi"
        img = self.dictionary.get_wiktionary_def_image("mother","en-hi","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-hi -> "+img

    def testEnglishKannada(self):
        self.dictionary.get_response()
        print "Testing English to Kananda"
        img = self.dictionary.get_wiktionary_def_image("mother","en-kn","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-kn -> "+img

    def testEnglishTelugu(self):
        self.dictionary.get_response()
        print "Testing Englsih to Telugu"
        img = self.dictionary.get_wiktionary_def_image("welcome","en-te","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-Te -> "+img

    def testEnglishMalayalam(self):
        self.dictionary.get_response()
        print "Testing English to Malayalam"
        img = self.dictionary.get_wiktionary_def_image("mother","en-ml","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-ml -> "+img

    def testEnglishTamil(self):
        self.dictionary.get_response()
        print "Testing English to Tamil"
        img = self.dictionary.get_wiktionary_def_image("mother","en-ta","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-ta -> "+img

    def testEnglishBengali(self):
        self.dictionary.get_response()
        print "Testing English to Bengali"
        img = self.dictionary.get_wiktionary_def_image("mother","en-bn","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-bn -> "+img

    def testEnglishGujarati(self):
        self.dictionary.get_response()
        print "Testing English to Gujarati"
        img = self.dictionary.get_wiktionary_def_image("mother","en-gu","png",0,0,color="Black",fontsize=10)
        self.assertNotEqual(img,"")
        print "En-gu -> "+img
        
        
if __name__ == "__main__":
    unittest.main()
