#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the UrlGenerator class.
"""
import unittest

from app.acclaim.badges.UrlGenerator import UrlGenerator


class UrlGeneratorTestCase(unittest.TestCase):
    def test_check_the_url(self):
        expected_url = 'https://www.youracclaim.com/organizations/TonyStark/badges?page={page}'

        url_generator = UrlGenerator('TonyStark')
        url = url_generator.url
        self.assertEqual(expected_url, url)

    def test_check_the_url_and_set_the_page_number(self):
        expected_url = 'https://www.youracclaim.com/organizations/Google/badges?page={page}'

        url_generator = UrlGenerator('Google', 87)
        url = url_generator.url
        self.assertEqual(expected_url, url)

    def test_get_the_urls(self):
        expected_url = [
            'https://www.youracclaim.com/organizations/Z/badges?page=1',
        ]

        url_generator = UrlGenerator('Z')
        urls = url_generator.get_urls
        self.assertEqual(expected_url, urls)

    def test_get_the_urls_given_a_limit(self):
        expected_url = [
            'https://www.youracclaim.com/organizations/Z/badges?page=5',
            'https://www.youracclaim.com/organizations/Z/badges?page=6',
            'https://www.youracclaim.com/organizations/Z/badges?page=7',
        ]

        url_generator = UrlGenerator('Z', start_at=5, end_at=7)
        urls = url_generator.get_urls
        self.assertEqual(expected_url, urls)


if __name__ == '__main__':
    unittest.main()
