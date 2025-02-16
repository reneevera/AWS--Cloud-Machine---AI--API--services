import os, sys
import unittest

import translation_service

class TranslationServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = translation_service.TranslationService()

    def test_translate_text(self):
        translation = self.service.translate_text('Einbahnstrabe')
        self.assertTrue(translation)
        self.assertEqual('de', translation['sourceLanguage'])
        # self.assertEqual('One way street', translation['translatedText'])
        self.assertEqual('One way street', translation['translatedText'])
        print('OK test for translation')
        

if __name__ == "__main__":
    unittest.main()