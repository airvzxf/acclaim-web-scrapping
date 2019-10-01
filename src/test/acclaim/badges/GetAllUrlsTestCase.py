#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the GetAllUrls class.
"""
import unittest
from unittest.mock import patch, call

from app.acclaim.badges.GetAllUrls import GetAllUrls


class GetAllUrlsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the Test Case.
        :rtype: None
        :return: None
        """
        self.company = 'KingKong'

        self.patch_url_generator = patch('app.acclaim.badges.UrlGenerator.UrlGenerator', autospec=True)
        self.MockUrlGenerator = self.patch_url_generator.start()

        self.patch_get_information = patch('app.acclaim.badges.GetInformation.GetInformation', autospec=True)
        self.MockGetInformation = self.patch_get_information.start()

    def tearDown(self) -> None:
        """
        Reset the test when it finish.
        :rtype: None
        :return: None
        """
        self.patch_url_generator.stop()
        self.patch_get_information.stop()

    def test_get_the_constant_badges_per_page(self):
        expected_badges_per_page = 48

        badges_per_page = GetAllUrls._BADGES_PER_PAGE
        self.assertEqual(expected_badges_per_page, badges_per_page)

    def test_call_the_class_url_generator(self):
        self.MockUrlGenerator.get_urls = ['']

        get_all = GetAllUrls(self.company)
        get_all.execute()
        self.MockUrlGenerator.assert_called_with(self.company)

    def test_call_the_class_url_generator_it_returns_empty_urls(self):
        self.MockUrlGenerator.return_value.get_urls = []

        get_all = GetAllUrls(self.company)
        executed = get_all.execute()
        self.assertEqual(False, executed)
        self.MockUrlGenerator.assert_called_with(self.company)

    def test_call_the_class_get_information(self):
        expected_url = 'The URL Badge'

        self.MockUrlGenerator.return_value.get_urls = [expected_url]

        get_all = GetAllUrls(self.company)
        get_all.execute()
        self.MockGetInformation.assert_called_with(expected_url)

    def test_get_number_of_badges(self):
        expected_badges = 1952

        self.MockUrlGenerator.return_value.get_urls = ['']
        self.MockGetInformation.return_value.badges = expected_badges

        get_all = GetAllUrls(self.company)
        get_all.execute()
        badges = get_all.get_badges
        self.assertEqual(expected_badges, badges)

    def test_get_number_of_pages(self):
        expected_pages = 3
        badges = 144  # 48 badges per page * 3 pages

        self.MockUrlGenerator.return_value.get_urls = ['']
        self.MockGetInformation.return_value.badges = badges

        get_all = GetAllUrls(self.company)
        get_all.execute()
        pages = get_all.get_pages
        self.assertEqual(expected_pages, pages)

    def test_get_number_of_pages_when_badges_are_a_below_number(self):
        expected_pages = 3
        badges = 143

        self.MockUrlGenerator.return_value.get_urls = ['']
        self.MockGetInformation.return_value.badges = badges

        get_all = GetAllUrls(self.company)
        get_all.execute()
        pages = get_all.get_pages
        self.assertEqual(expected_pages, pages)

    def test_get_generated_urls(self):
        expected_pages = 2
        expected_urls = [
            'Url with page one',
            'Url with page two',
            'Url with page three',
            'Url with page four',
        ]
        expected_url_generator_calls = [
            call(self.company),
            call(self.company, end_at=expected_pages)
        ]
        badges = 49

        self.MockUrlGenerator.return_value.get_urls = expected_urls
        self.MockGetInformation.return_value.badges = badges

        get_all = GetAllUrls(self.company)
        get_all.execute()
        urls = get_all.get_urls
        self.assertEqual(expected_urls, urls)
        self.MockUrlGenerator.assert_has_calls(expected_url_generator_calls)
