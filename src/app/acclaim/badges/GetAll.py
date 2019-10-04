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
    _urls = []
    _number_of_badges = 0
    _multiprocess = True
    _max_workers = None
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
        self._badges_id = []
        get_all_urls = GetAllUrls(self.company)
        if not get_all_urls.execute():
            return False
        self._number_of_badges = get_all_urls.get_badges
        self._urls = get_all_urls.get_urls
        if len(self._urls) < 1:
            return False
        self._multiprocessing_badges(self._multiprocess)
        return True

    def _multiprocessing_badges(self, multiprocess: bool = True) -> None:
        """
        Get the badges using single or multi processing.
        :type multiprocess: bool
        :param multiprocess: If it's true then use multiprocessing other wise use a single processor.
        :rtype: None
        :return: None
        """
        from concurrent.futures.thread import ThreadPoolExecutor
        from time import time
        if multiprocess is False:
            for url in self._urls:
                self._badges_id += self._request_urls(url)
        else:
            init_time = time()
            processors = self._max_workers
            if processors:
                number_of_urls = len(self._urls)
                if number_of_urls <= 0:
                    processors = None
                elif number_of_urls < processors:
                    processors = number_of_urls

            executor = ThreadPoolExecutor(processors)
            pages_with_badges = executor.map(self._request_urls, self._urls)

            difference = int(time() - init_time)
            print('# -------------------------------------------')
            print('# Execution time: ', difference)
            print('# -------------------------------------------')
            for badges_id in pages_with_badges:
                self._badges_id += badges_id
        self._number_of_badges = len(self._badges_id)

    def _request_urls(self, url: str) -> list:
        """
        Request an URL and return the badges id.
        :type url: str
        :param url: Web page URL with the badges.
        :rtype: list
        :return: Return a list with the badges IDs.
        """
        from urllib3 import PoolManager
        from re import findall
        http = PoolManager()
        response = http.request('GET', url)
        try:
            data = response.data.decode('utf-8')
        except AttributeError:
            return []
        return findall(self._REGULAR_EXPRESSION, data)

    @property
    def get_number_of_badges(self) -> int:
        """
        Return the number of badges.
        :rtype: int
        :return: Number of badges
        """
        return self._number_of_badges

    @property
    def get_badges_id(self) -> list:
        """
        Return all the badges ids.
        :rtype: list
        :return: Badges IDs.
        """
        return self._badges_id
