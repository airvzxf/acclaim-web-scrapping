#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the HttpRequest class.
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from app.HttpRequest import HttpRequest


class HttpRequestTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up the Test Case.
        :rtype: None
        :return: None
        """
        self.url_1 = 'https://fake.me'
        self.status_1 = 10101
        self.data_1 = b'My body is not fake'
        self.data_json_1 = b'{' \
                           b'"data":[{"hi":"Man"}, {"orko":null}],' \
                           b'"metadata":[{"imagine": 1}, {"people": "Yes"}]' \
                           b'}'

        self.url_2 = 'https://fake-news.org'
        self.status_2 = 9999
        self.data_2 = b'I am not new!'
        self.data_json_2 = b'{' \
                           b'"nothing":[{"no":true}, {"thing":false}]' \
                           b'}'

        self.data_json_empty = {}

    def test_assign_the_url_variable(self):
        http_request = HttpRequest(url=self.url_1)
        self.assertEqual(self.url_1, http_request.url)

    @patch('urllib3.PoolManager.request')
    def test_request_url_and_get_the_response(self, urllib3_patch):
        mock_urllib3 = Mock()
        mock_urllib3.status = self.status_1
        mock_urllib3.data = None
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        response = http_request.request()
        self.assertEqual(self.status_1, response)

    @patch('urllib3.PoolManager.request')
    def test_request_another_url_and_get_the_response(self, urllib3_patch):
        mock_urllib3 = Mock()
        mock_urllib3.status = self.status_2
        mock_urllib3.data = None
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_2)
        response = http_request.request()
        self.assertEqual(self.status_2, response)

    @patch('urllib3.PoolManager.request')
    def test_get_response_data(self, urllib3_patch):
        mock_urllib3 = Mock()
        mock_urllib3.data = self.data_1
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data = http_request.data
        self.assertEqual(self.data_1, data)

    @patch('urllib3.PoolManager.request')
    def test_get_response_data_with_json_object(self, urllib3_patch):
        from json import loads
        expected_data_json = loads('{"nothing":[{"no":true}, {"thing":false}]}')

        mock_urllib3 = Mock()
        mock_urllib3.data = self.data_json_2
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(expected_data_json, data_json)

    @patch('urllib3.PoolManager.request')
    def test_get_response_data_with_invalid_json_object(self, urllib3_patch):
        expected_data_json = self.data_json_empty

        mock_urllib3 = Mock()
        mock_urllib3.data = self.data_1
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(expected_data_json, data_json)

    @patch('urllib3.PoolManager.request')
    def test_get_response_invalid_data_check_the_json_object(self, urllib3_patch):
        mock_urllib3 = Mock()
        mock_urllib3.data = None
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(self.data_json_empty, data_json)

    @patch('urllib3.PoolManager.request')
    def test_get_response_json_for_data_object(self, urllib3_patch):
        from json import loads
        expected_data_json = loads('{"data":[{"hi":"Man"}, {"orko":null}]}')['data']

        mock_urllib3 = Mock()
        mock_urllib3.data = self.data_json_1
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.get_data_json_by('data')
        self.assertEqual(expected_data_json, data_json)

    @patch('urllib3.PoolManager.request')
    def test_get_response_json_for_data_object_when_not_exists(self, urllib3_patch):
        mock_urllib3 = Mock()
        mock_urllib3.data = self.data_json_2
        urllib3_patch.return_value = mock_urllib3

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.get_data_json_by('data')
        self.assertEqual(self.data_json_empty, data_json)
