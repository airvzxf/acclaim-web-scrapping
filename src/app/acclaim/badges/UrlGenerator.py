#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to generate the URL badge links from the Acclaim web site.
"""


class UrlGenerator:
    """"
    Generate the URL badge links from the Acclaim web site.
    """

    def __init__(self, company: str, start_at: int = 1, end_at: int = None) -> None:
        """
        Init the class
        :type company: str
        :param company: The company parameter.
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

        self.url = 'https://www.youracclaim.com/organizations/' + \
                   '{company}/badges?'.format(company=company, ) + \
                   'page={page}'

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
