#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the TextExtraction class.
"""
from unittest import TestCase

from app.tool.TextExtraction import TextExtraction


class TextExtractionTestCase(TestCase):
    def test_extract_a_text(self):
        text = 'Hello Bing, I need Bing for the Bang.'
        regex = r'(Bing)'
        expected_matches = ['Bing', 'Bing']

        text_extraction = TextExtraction(text, regex)
        matches = text_extraction.matches
        self.assertEqual(expected_matches, matches)

    def test_extract_text_case_insensitive(self):
        text = 'Lets go. I want to Go! Do you go?'
        regex = r'(go)'
        expected_matches = ['go', 'Go', 'go']

        text_extraction = TextExtraction(text, regex)
        matches = text_extraction.matches
        self.assertEqual(expected_matches, matches)
