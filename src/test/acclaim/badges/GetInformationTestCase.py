#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the GetInformation class.
"""
from unittest import TestCase
from unittest.mock import patch

from app.acclaim.badges.GetInformation import GetInformation


class GetInformationTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up the Test Case.
        :rtype: None
        :return: None
        """
        self.patch_urllib3 = patch('urllib3.PoolManager', autospec=True)
        self.MockUrllib3 = self.patch_urllib3.start()
        self.MockUrllib3_request = self.MockUrllib3.return_value.request.return_value

    def tearDown(self) -> None:
        """
        Reset the test when it finish.
        :rtype: None
        :return: None
        """
        self.patch_urllib3.stop()

    def test_get_number_of_badges(self):
        expected_badges = 1952
        response_data = bytes(
            'This is a cool test {badges} badges in our property.'.format(badges=expected_badges),
            'utf-8')

        self.MockUrllib3_request.data = response_data

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    def test_when_the_page_not_has_the_information(self):
        expected_badges = 0
        response_data = b'Anything here.'

        self.MockUrllib3_request.data = response_data

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    def test_when_the_data_response_is_wrong(self):
        expected_badges = 0

        self.MockUrllib3_request.data = False

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)
