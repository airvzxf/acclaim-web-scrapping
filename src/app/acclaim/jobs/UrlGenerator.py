#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to generate the URL job links from the Acclaim web site.
"""


class UrlGenerator:
    """"
    Generate the URL job links from the Acclaim web site.
    """

    def __init__(self,
                 company: str,
                 badge: str,
                 country: str,
                 salary_ranges: int,
                 start_at: int = 1,
                 end_at: int = None,
                 ) -> None:

        """
        Init the class
        :type company: str
        :param company: The company name.
        :type badge: str
        :param badge: The badge ID / alias.
        :type country: str
        :param country: The country code with two letters.
        :type salary_ranges: int
        :param salary_ranges: The salary range ID.
        :type start_at: int
        :param start_at: The page number where it starts the gathering.
        :type end_at: int
        :param end_at: The page number where it finishes the gathering.
        :rtype: None
        :return: None
        """
        self.start_at = start_at

        if end_at:
            self.end_at = end_at
        else:
            self.end_at = start_at

        self.url = 'https://www.youracclaim.com/api/v1/jobs/' + \
                   '{company}/'.format(company=company) + \
                   '{badge}?'.format(badge=badge) + \
                   'country={country}&'.format(country=country) + \
                   'salary_ranges[id]={salary_ranges}&'.format(salary_ranges=salary_ranges) + \
                   'salary_ranges[name]=&' + \
                   'page={page}&'

    @property
    def get_urls(self) -> list:
        """
        Get the URLs generated with the given parameters.
        :rtype: list
        :return: The list of the generated URLS.
        """
        urls = []
        for page in range(self.start_at, self.end_at + 1):
            urls.append(self.url.format(page=page))
        return urls
