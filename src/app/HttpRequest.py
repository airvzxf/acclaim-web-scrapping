#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Class to request an url and return the response.
"""


class HttpRequest:
    """
    Handle the HTTP request and get a response.
    """

    def __init__(self, url: str) -> None:
        """
        Init the class.
        :type url: str
        :param url: A valid URL with http or https.
        :rtype: None
        :return: None
        """
        self.url = url
        self._response = None
        self._data_json = {}

    def request(self) -> int:
        """
        Return the response of the request.
        :rtype: int
        :return: The response
        """
        from urllib3 import PoolManager
        http = PoolManager()
        self._response = http.request('GET', self.url)
        self._data_json = self.__convert_data_to_json
        return self._response.status

    @property
    def __convert_data_to_json(self) -> dict:
        """
        Convert the data response into JSON with the properly validations.
        :rtype: dict
        :return: Python dictionary with the JSON values.
        """
        from json import loads
        try:
            self._data_json = loads(self._response.data.decode('utf-8'))
        except (AttributeError, ValueError):
            return {}
        return self._data_json

    @property
    def data(self) -> bytes:
        """
        Return the data from the request.
        :rtype: bytes
        :return: The data
        """
        return self._response.data

    @property
    def data_json(self) -> dict:
        """
        Return the data JSON
        :rtype: dict
        :return: A dictionary with the JSON information.
        """
        return self._data_json

    def get_data_json_by(self, object_id: str) -> dict:
        """"
        Return the JSON object with the data object if it exists.
        :type object_id: str
        :param object_id: The JSON key id.
        :rtype: dict
        :return: The data
        """
        if object_id in self._data_json.keys():
            return self._data_json[object_id]
        return {}
