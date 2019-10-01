#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to extract text from the other text.
"""


class TextExtraction:
    """
    Extract an specific text from the other text.
    """
    text = None
    regex = None

    def __init__(self, text: str, regex: str) -> None:
        """
        Init the class
        :type text: str
        :param text: The source text.
        :type text: str
        :param text: The regular expression for search the matches.
        :rtype: None
        :return: None
        """
        self.text = text
        self.regex = regex

    @property
    def matches(self) -> list:
        """
        Return the matches found in the text.
        :rtype: list
        :return: List with the matches
        """
        from re import findall, IGNORECASE
        matches = findall(self.regex, self.text, IGNORECASE)
        return matches
