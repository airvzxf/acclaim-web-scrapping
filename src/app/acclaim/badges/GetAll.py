#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to get all the badges id's.
"""


class GetAll:
    """"
    Generate the ID badges.
    """
    _REGULAR_EXPRESSION = r'c-grid-item c-grid-item--stack-lt-sm cr-public-organization-badge-template-grid-item.* ' + \
                          'href="/org/{company}/badge/([^"]+)"'
    _badges_id = []
    company = None

    def __init__(self, company: str) -> None:
        """
        Init the class
        :type company: str
        :param company: The company parameter.
        :rtype: None
        :return: None
        """
        self.company = company
        self._REGULAR_EXPRESSION = self._REGULAR_EXPRESSION.format(company=company)

    def execute(self) -> bool:
        """
        Start the process to get all the badges id's.
        :rtype: bool
        :return: True if the process is completed and all the badges were retrieved.
        """
        from app.acclaim.badges.GetAllUrls import GetAllUrls
        from urllib3 import PoolManager
        from re import findall
        self._badges_id = []
        get_all_urls = GetAllUrls(self.company)
        if not get_all_urls.execute():
            return False
        http = PoolManager()
        for url in get_all_urls.get_urls:
            response = http.request('GET', url)
            try:
                data = response.data.decode('utf-8')
            except AttributeError:
                continue
            self._badges_id += findall(self._REGULAR_EXPRESSION, data)
        return True

    @property
    def get_badges_id(self) -> list:
        """
        Return all the badges ids.
        :rtype: list
        :return: Badges IDs.
        """
        return self._badges_id
