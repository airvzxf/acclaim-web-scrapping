#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to get the main information for the badges.
"""


class GetInformation:
    """"
    Get how many badges are for the specific company.
    """

    def __init__(self, url: str) -> None:
        """
        Init the class.
        :type url: str
        :param url: A valid URL with http or https.
        :rtype: None
        :return: None
        """
        from urllib3 import PoolManager
        http = PoolManager()
        self._response = http.request('GET', url)
        self.badges = self.__get_badges

    @property
    def __get_badges(self) -> int:
        from re import findall, IGNORECASE
        regex = r'(\d+) badges'
        try:
            data = self._response.data.decode('utf-8')
        except AttributeError:
            return 0
        try:
            badges = int(findall(regex, data, IGNORECASE)[0])
        except IndexError:
            return 0
        return badges


if __name__ == "__main__":
    info = GetInformation('https://www.youracclaim.com/organizations/ibm/badges')
    badges = info.badges
    print('badges: ', badges)
    pass
