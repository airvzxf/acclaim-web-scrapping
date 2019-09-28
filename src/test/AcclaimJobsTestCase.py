#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Unit Test for the AcclaimJobs class.
"""
import unittest

from app.AcclaimJobs import AcclaimJobs


class AcclaimJobsTestCase(unittest.TestCase):
    def test_check_the_url(self):
        expected_url = 'https://www.youracclaim.com/api/v1/jobs/' + \
                       'TonyStark/' + \
                       'NotLooser?' \
                       'country=MX&' + \
                       'salary_ranges[id]=9&' + \
                       'salary_ranges[name]=&' + \
                       'page={page}&'
        acclaim_jobs = AcclaimJobs('TonyStark', 'NotLooser', 'MX', 9)
        url = acclaim_jobs.url
        self.assertEqual(expected_url, url)

    def test_check_the_url_and_set_the_page_number(self):
        expected_url = 'https://www.youracclaim.com/api/v1/jobs/' + \
                       'TonyStark/' + \
                       'NotLooser?' \
                       'country=MX&' + \
                       'salary_ranges[id]=9&' + \
                       'salary_ranges[name]=&' + \
                       'page={page}&'
        acclaim_jobs = AcclaimJobs('TonyStark', 'NotLooser', 'MX', 9, 55, 80)
        url = acclaim_jobs.url
        self.assertEqual(expected_url, url)

    def test_get_the_urls(self):
        expected_url = [
            'https://www.youracclaim.com/api/v1/jobs/Z/j-l?country=AB&salary_ranges[id]=101&salary_ranges[name]=&' +
            'page=1&',
        ]
        acclaim_jobs = AcclaimJobs('Z', 'j-l', 'AB', 101)
        urls = acclaim_jobs.get_urls
        self.assertEqual(expected_url, urls)

    def test_get_the_urls_given_a_limit(self):
        expected_url = [
            'https://www.youracclaim.com/api/v1/jobs/Z/j-l?country=AB&salary_ranges[id]=101&salary_ranges[name]=&' +
            'page=39&',
            'https://www.youracclaim.com/api/v1/jobs/Z/j-l?country=AB&salary_ranges[id]=101&salary_ranges[name]=&' +
            'page=40&',
            'https://www.youracclaim.com/api/v1/jobs/Z/j-l?country=AB&salary_ranges[id]=101&salary_ranges[name]=&' +
            'page=41&',
            'https://www.youracclaim.com/api/v1/jobs/Z/j-l?country=AB&salary_ranges[id]=101&salary_ranges[name]=&' +
            'page=42&',
        ]
        acclaim_jobs = AcclaimJobs('Z', 'j-l', 'AB', 101, 39, 42)
        urls = acclaim_jobs.get_urls
        self.assertEqual(expected_url, urls)


if __name__ == '__main__':
    unittest.main()
