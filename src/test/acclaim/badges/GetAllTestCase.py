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
        self.MockGetAllUrls_execute = self.MockGetAllUrls.return_value.execute

        self.patch_urllib3 = patch('urllib3.PoolManager', autospec=True)
        self.MockUrllib3 = self.patch_urllib3.start()
        # TODO: Do I'll use this request and requested?
        self.MockUrllib3_request = self.MockUrllib3.return_value.request
        self.MockUrllib3_requested = self.MockUrllib3_request.return_value

        # self.patch_re = patch('re', autospec=True)
        # self.MockRe = self.patch_re.start()
        # # TODO: Do I'll use this find_all and found_all?
        # self.MockRe_find_all = self.MockRe.return_value.findall
        # self.MockRe_found_all = self.MockRe_find_all.return_value

    def tearDown(self) -> None:
        """
        Reset the test when it finish.
        :rtype: None
        :return: None
        """
        self.patch_get_all_urls.stop()
        self.patch_urllib3.stop()

    def test_instance_the_company_attribute(self):
        get_all = GetAll(self.company)
        company = get_all.company
        self.assertEqual(self.company, company)

    def test_replace_the_company_in_the_regular_expression(self):
        expected_url = r'c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-template-grid-item.* ' + \
                       'href="/org/{company}/badge/([^"]+)"'.format(company=self.company)

        get_all = GetAll(self.company)
        url = get_all._REGULAR_EXPRESSION
        self.assertEqual(expected_url, url)

    def test_call_the_class_get_all_urls(self):
        get_all = GetAll(self.company)
        get_all.execute()
        self.MockGetAllUrls.assert_called_once_with(self.company)
        self.MockGetAllUrls_execute.assert_called_once()

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
        get_all.execute()
        self.MockUrllib3_request.assert_has_calls(expected_calls)

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

        self.MockGetAllUrls.return_value.get_urls = urls
        self.MockUrllib3_requested.data.decode.side_effect = responses

        get_all = GetAll(self.company)
        get_all.execute()
        badges_ids = get_all.get_badges_id
        self.assertEqual(expected_badges_ids, badges_ids)

    def test_get_two_valid_bades_id(self):
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
        get_all.execute()
        badges_ids = get_all.get_badges_id
        self.assertEqual(expected_badges_ids, badges_ids)
