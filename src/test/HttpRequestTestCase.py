#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the HttpRequest class.
"""
from unittest import TestCase
from unittest.mock import patch

from app.HttpRequest import HttpRequest


class HttpRequestTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up the Test Case.
        :rtype: None
        :return: None
        """
        self.patch_urllib3 = patch('urllib3.PoolManager')
        self.MockUrllib3 = self.patch_urllib3.start()
        self.MockUrllib3_request = self.MockUrllib3.return_value.request.return_value

        self.url_1 = 'https://fake.me'
        self.status_1 = 10101
        self.data_1 = b'My body is not fake'
        self.data_json_1 = b'{' \
                           b'"data":[{"hi":"Man"}, {"orko":null}],' \
                           b'"metadata":[{"imagine": 1}, {"people": "Yes"}]' \
                           b'}'

        self.url_2 = 'https://fake-news.org'
        self.status_2 = 9999
        self.data_json_2 = b'{' \
                           b'"nothing":[{"no":true}, {"thing":false}]' \
                           b'}'

        self.data_json_empty = {}

    def tearDown(self) -> None:
        """
        Reset the test when it finish.
        :rtype: None
        :return: None
        """
        self.patch_urllib3.stop()

    def test_assign_the_url_variable(self):
        http_request = HttpRequest(url=self.url_1)
        self.assertEqual(self.url_1, http_request.url)

    def test_request_url_and_get_the_response(self):
        self.MockUrllib3_request.status = self.status_1
        self.MockUrllib3_request.data = None

        http_request = HttpRequest(url=self.url_1)
        response = http_request.request()
        self.assertEqual(self.status_1, response)

    def test_request_another_url_and_get_the_response(self):
        self.MockUrllib3_request.status = self.status_2
        self.MockUrllib3_request.data = None

        http_request = HttpRequest(url=self.url_2)
        response = http_request.request()
        self.assertEqual(self.status_2, response)

    def test_get_response_data(self):
        self.MockUrllib3_request.data = self.data_1

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data = http_request.data
        self.assertEqual(self.data_1, data)

    def test_get_response_data_with_json_object(self):
        from json import loads
        expected_data_json = loads('{"nothing":[{"no":true}, {"thing":false}]}')

        self.MockUrllib3_request.data = self.data_json_2

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(expected_data_json, data_json)

    def test_get_response_data_with_invalid_json_object(self):
        expected_data_json = self.data_json_empty

        self.MockUrllib3_request.data = self.data_1

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(expected_data_json, data_json)

    def test_get_response_invalid_data_check_the_json_object(self):
        self.MockUrllib3_request.data = None

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.data_json
        self.assertEqual(self.data_json_empty, data_json)

    def test_get_response_json_for_data_object(self):
        from json import loads
        expected_data_json = loads('{"data":[{"hi":"Man"}, {"orko":null}]}')['data']

        self.MockUrllib3_request.data = self.data_json_1

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.get_data_json_by('data')
        self.assertEqual(expected_data_json, data_json)

    def test_get_response_json_for_data_object_when_not_exists(self):
        self.MockUrllib3_request.data = self.data_json_2

        http_request = HttpRequest(url=self.url_1)
        http_request.request()
        data_json = http_request.get_data_json_by('data')
        self.assertEqual(self.data_json_empty, data_json)
