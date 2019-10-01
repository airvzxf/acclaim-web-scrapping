#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the GetInformation class.
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from app.acclaim.badges.GetInformation import GetInformation


# TODO: Move Mock Patch into a setup function.
class GetInformationTestCase(TestCase):
    @patch('urllib3.PoolManager', autospec=True)
    def test_get_number_of_badges(self, mock_urllib3):
        expected_badges = 1952
        response_data = bytes(
            'This is a cool test {badges} badges in our property.'.format(badges=expected_badges),
            'utf-8')

        mock_urllib3.return_value = Mock()
        mock_urllib3_class_request = mock_urllib3.return_value.request.return_value
        mock_urllib3_class_request.data = response_data

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    @patch('urllib3.PoolManager', autospec=True)
    def test_when_the_page_not_has_the_information(self, mock_urllib3):
        expected_badges = 0
        response_data = b'Anything here.'

        mock_urllib3.return_value = Mock()
        mock_urllib3_class_request = mock_urllib3.return_value.request.return_value
        mock_urllib3_class_request.data = response_data

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    @patch('urllib3.PoolManager', autospec=True)
    def test_when_the_data_response_is_wrong(self, mock_urllib3):
        expected_badges = 0

        mock_urllib3.return_value = Mock()
        mock_urllib3_class_request = mock_urllib3.return_value.request.return_value
        mock_urllib3_class_request.data = False

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)
