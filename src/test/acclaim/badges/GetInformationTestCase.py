import unittest
from unittest import TestCase
from unittest.mock import patch

from app.acclaim.badges.GetInformation import GetInformation
from test.mock_system.MockUrllib3 import MockUrllib3


class GetInformationTestCase(TestCase):
    @patch('urllib3.PoolManager.request')
    def test_get_number_of_badges(self, urllib3_patch):
        expected_badges = 1952
        response_data = bytes(
            'This is a cool test {badges} badges in our property.'.format(badges=expected_badges),
            'utf-8')

        mock_urllib3 = MockUrllib3()
        mock_urllib3.data = response_data
        urllib3_patch.return_value = mock_urllib3

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    @patch('urllib3.PoolManager.request')
    def test_when_the_page_not_has_the_information(self, urllib3_patch):
        expected_badges = 0
        response_data = b'Anything here.'

        mock_urllib3 = MockUrllib3()
        mock_urllib3.data = response_data
        urllib3_patch.return_value = mock_urllib3

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)

    @patch('urllib3.PoolManager.request')
    def test_when_the_data_response_is_wrong(self, urllib3_patch):
        expected_badges = 0

        mock_urllib3 = MockUrllib3()
        mock_urllib3.data = False
        urllib3_patch.return_value = mock_urllib3

        get_information = GetInformation('Any url')
        badges = get_information.badges
        self.assertEqual(expected_badges, badges)


if __name__ == '__main__':
    unittest.main()
