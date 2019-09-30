#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to get all the badges from a specific company by page number.
"""


class GetAll:
    """"
    Get all the badges from a specific company by page number.
    """
    badges_per_page = 48

    def __init__(self, company: str) -> None:
        """
        Init the class.
        :type company: str
        :param company: The company.
        :rtype: None
        :return: None
        """
        self.company = company
        self.badges = 0
        self.urls = []

    def execute(self) -> bool:
        """
        Start the process to check if exists badges for the specific company,
        get the number of badges and the maximum number of pages.
        :rtype: bool
        :return: True if the process is completed and all the information was retrieved.
        """
        from app.acclaim.badges.GetInformation import GetInformation
        from app.acclaim.badges.UrlGenerator import UrlGenerator
        url_generator = UrlGenerator(self.company)
        try:
            main_page = url_generator.get_urls[0]
        except IndexError:
            return False
        get_information = GetInformation(main_page)
        self.badges = get_information.badges
        return True

    @property
    def get_badges(self) -> int:
        """
        Return the number of badges found for the company.
        :rtype: int
        :return: Number of badges found.
        """
        return self.badges

    @property
    def get_pages(self) -> int:
        """
        Return the max number of pages where the badges are indexed.
        :rtype: int
        :return: Max number of pages.
        """
        from math import ceil
        return ceil(self.badges / self.badges_per_page)

    @property
    def get_urls(self) -> list:
        """
        Return the list with all the URLS that means from page 1 to the max page.
        :rtype: list
        :return: The list with the URLS.
        """
        from app.acclaim.badges.UrlGenerator import UrlGenerator
        url_generator = UrlGenerator(self.company, end_at=self.get_pages)
        urls = url_generator.get_urls
        return urls
