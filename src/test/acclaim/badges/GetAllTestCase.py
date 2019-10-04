#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the GetAll class.
"""
import unittest
from unittest.mock import patch, call

from app.acclaim.badges.GetAll import GetAll


class GetAllUrlsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the Test Case.
        :rtype: None
        :return: None
        """
        self.company = 'Massimo'

        self.patch_get_all_urls = patch('app.acclaim.badges.GetAllUrls.GetAllUrls', autospec=True)
        self.MockGetAllUrls = self.patch_get_all_urls.start()

        self.patch_urllib3 = patch('urllib3.PoolManager', autospec=True)
        self.MockUrllib3 = self.patch_urllib3.start()
        self.MockUrllib3_request = self.MockUrllib3.return_value.request
        self.MockUrllib3_requested = self.MockUrllib3_request.return_value
        self.MockGetAllUrls_execute = self.MockGetAllUrls.return_value.execute

        self.patch_thread_pool_executor = patch('concurrent.futures.thread.ThreadPoolExecutor', autospec=True)
        self.MockThreadPoolExecutor = self.patch_thread_pool_executor.start()
        self.MockThreadPoolExecutor_map = self.MockThreadPoolExecutor.return_value.map

    def tearDown(self) -> None:
        """
        Reset the test when it finish.
        :rtype: None
        :return: None
        """
        self.patch_get_all_urls.stop()
        self.patch_urllib3.stop()
        self.patch_thread_pool_executor.stop()

    def test_the_company_attribute_in_the_instance(self):
        get_all = GetAll(self.company)
        company = get_all.company
        self.assertEqual(self.company, company)

    def test_replace_the_company_in_the_regular_expression(self):
        expected_url = r'c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-template-grid-item.* ' + \
                       'href="/org/{company}/badge/([^"]+)"'.format(company=self.company)

        get_all = GetAll(self.company)
        url = get_all._REGULAR_EXPRESSION
        self.assertEqual(expected_url, url)

    def test_get_number_of_badges_from_the_class_get_all_urls(self):
        expected_badges = 29843

        self.MockGetAllUrls.return_value.get_badges = expected_badges

        get_all = GetAll(self.company)
        get_all._multiprocessing_badges = lambda x: x
        get_all.execute()
        number_of_badges = get_all.get_number_of_badges
        self.assertEqual(expected_badges, number_of_badges)

    def test_call_the_class_get_all_urls(self):
        get_all = GetAll(self.company)
        get_all.execute()
        self.MockGetAllUrls.assert_called_once_with(self.company)
        self.MockGetAllUrls_execute.assert_called_once()

    def test_when_get_zero_urls(self):
        expected_executed = False

        self.MockGetAllUrls.return_value.get_urls = []

        get_all = GetAll(self.company)
        executed = get_all.execute()
        self.assertEqual(expected_executed, executed)

    def test_when_an_invalid_call_the_class_get_all_urls_returns_false(self):
        expected_executed = False

        self.MockGetAllUrls_execute.return_value = False

        get_all = GetAll(self.company)
        executed = get_all.execute()
        self.assertEqual(expected_executed, executed)

    def test_when_an_invalid_call_the_class_get_all_urls_returns_an_empty_badges_id(self):
        expected_badges = []

        self.MockGetAllUrls_execute.return_value = False

        get_all = GetAll(self.company)
        get_all._badges_id = None  # Be sure that it's returning an empty list
        get_all.execute()
        badges = get_all.get_badges_id
        self.assertEqual(expected_badges, badges)

    def test_request_all_the_urls(self):
        urls = [
            'Url #1',
            'Url #2',
            'Url #3',
        ]
        expected_calls = [
            call('GET', urls[0]),
            call('GET', urls[1]),
            call('GET', urls[2]),
        ]

        self.MockGetAllUrls.return_value.get_urls = urls
        self.MockUrllib3_requested.data = b''

        get_all = GetAll(self.company)
        get_all._multiprocess = False
        get_all.execute()
        self.MockUrllib3_request.assert_has_calls(expected_calls)

    def test_get_the_badges_id(self):
        base_url = r'<div class="c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-' + \
                   r'template-grid-item" href="/org/{company}/badge/'.format(company=self.company) + \
                   r'{badge_id}">Nothing</div>'
        badges_ids = [
            'hello-world',
            'Nikki-93-Micah',
            'what.eVer.123',
        ]
        urls = [
            'Url #1',
            'Url #2',
            'Url #3',
        ]
        responses = [
            base_url.format(badge_id=badges_ids[0]),
            base_url.format(badge_id=badges_ids[1]),
            base_url.format(badge_id=badges_ids[2]),
        ]
        expected_badges_ids = [
            badges_ids[0],
            badges_ids[1],
            badges_ids[2],
        ]
        expected_badges = len(badges_ids)

        self.MockGetAllUrls.return_value.get_urls = urls
        self.MockUrllib3_requested.data.decode.side_effect = responses

        get_all = GetAll(self.company)
        get_all._multiprocess = False
        get_all.execute()
        badges_ids = get_all.get_badges_id
        number_of_badges = get_all.get_number_of_badges
        self.assertEqual(expected_badges_ids, badges_ids)
        self.assertEqual(expected_badges, number_of_badges)

    def test_get_two_valid_badges_id(self):
        base_url = r'<div class="c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-' + \
                   r'template-grid-item" href="/org/{company}/badge/'.format(company=self.company) + \
                   r'{badge_id}">Nothing</div>'
        badges_ids = [
            'hello-world',
            '"></spam class="Nikki-93-Micah',
            'what.eVer.123',
        ]
        urls = [
            'Url #1',
            'Url #2',
            'Url #3',
        ]
        responses = [
            base_url.format(badge_id=badges_ids[0]),
            base_url.format(badge_id=badges_ids[1]),
            base_url.format(badge_id=badges_ids[2]),
        ]
        expected_badges_ids = [
            badges_ids[0],
            badges_ids[2],
        ]

        self.MockGetAllUrls.return_value.get_urls = urls
        self.MockUrllib3_requested.data.decode.side_effect = responses

        get_all = GetAll(self.company)
        get_all._multiprocess = False
        get_all.execute()
        badges_ids = get_all.get_badges_id
        self.assertEqual(expected_badges_ids, badges_ids)

    def test_when_the_data_request_is_invalid(self):
        urls = [
            'Url #1',
            'Url #2',
            'Url #3',
        ]
        expected_calls = [
            call('GET', urls[0]),
            call('GET', urls[1]),
            call('GET', urls[2]),
        ]

        self.MockGetAllUrls.return_value.get_urls = urls
        self.MockUrllib3_requested.data = None

        get_all = GetAll(self.company)
        get_all._multiprocess = False
        get_all.execute()
        self.MockUrllib3_request.assert_has_calls(expected_calls)

    def test_multiprocessor(self):
        urls = [
            'Url #1',
            'Url #2',
            'Url #3',
        ]

        get_all = GetAll(self.company)
        get_all._urls = urls
        get_all._multiprocessing_badges()
        self.MockThreadPoolExecutor_map.assert_called_once_with(get_all._request_urls, get_all._urls)

    def test_multiprocessor_when_max_workers_is_None_and_number_of_badges_exists(self):
        expected_max_processor = None

        get_all = GetAll(self.company)
        get_all._number_of_badges = 1987
        get_all._multiprocessing_badges()
        self.MockThreadPoolExecutor.assert_called_once_with(expected_max_processor)

    def test_multiprocessor_when_max_workers_is_greater_than_badges_but_badges_is_zero(self):
        expected_max_processor = 999
        badges = 0
        expected_processor = None

        get_all = GetAll(self.company)
        get_all._max_workers = expected_max_processor
        get_all._number_of_badges = badges
        get_all._multiprocessing_badges()
        self.MockThreadPoolExecutor.assert_called_once_with(expected_processor)

    def test_multiprocessor_when_max_workers_is_greater_than_badges(self):
        max_workers = 999
        urls = ['', '', '', '', '', ]
        expected_workers = len(urls)

        get_all = GetAll(self.company)
        get_all._max_workers = max_workers
        get_all._urls = urls
        get_all._multiprocessing_badges()
        self.MockThreadPoolExecutor.assert_called_once_with(expected_workers)

    def test_multiprocessor_when_max_workers_is_less_than_badges(self):
        urls = ['', '', '', '', '', ]
        expected_workers = 2

        get_all = GetAll(self.company)
        get_all._max_workers = expected_workers
        get_all._urls = urls
        get_all._multiprocessing_badges()
        self.MockThreadPoolExecutor.assert_called_once_with(expected_workers)

    def test_multiprocessor_get_badges_ids(self):
        badges_1 = [
            'hello-world',
            'Nikki-93-Micah',
            'what.eVer.123',
        ]
        badges_2 = [
            'cool',
            'I-am-badge'
        ]
        pages_with_badges = [
            badges_1,
            badges_2
        ]
        expected_badges_id = badges_1 + badges_2

        self.MockThreadPoolExecutor_map.return_value = pages_with_badges

        get_all = GetAll(self.company)
        get_all._multiprocessing_badges()
        self.assertEqual(expected_badges_id, get_all._badges_id)
