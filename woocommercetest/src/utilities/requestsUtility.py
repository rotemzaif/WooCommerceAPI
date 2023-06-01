from woocommercetest.src.configs.hosts_config import API_HOSTS
from woocommercetest.src.utilities.credentialsUtility import CredentialsUtility
import os
import logging as logger
from requests_oauthlib import OAuth1
import requests


class RequestUtility(object):
    def __init__(self):
        wc_cred = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = API_HOSTS[self.env]
        self.auth = OAuth1(wc_cred['wc_key'], wc_cred['wc_secret'])

    @staticmethod
    def assert_status_code(response, expected_status_code, url):
        assert response.status_code == expected_status_code, f"Wrong status code. Expected {expected_status_code},  Actual: {response.status_code}," \
                                                             f"URL: {url}, response json: {response.json()}"

    def post(self, endpoint, req_topic, payload=None, headers=None, expected_status_code=200):
        if not headers:
            headers = {"Content-Type": "application/json"}
        url = self.base_url + endpoint
        response = requests.post(url=url, json=payload, headers=headers, auth=self.auth)
        self.assert_status_code(response, expected_status_code, url)
        logger.debug(f"Sent POST REQUEST '{req_topic}' API response: {response.json()}")
        return response.json()

    def get(self, endpoint, req_topic, payload=None, headers=None, expected_status_code=200, params=None):
        if not headers:
            headers = {"Content-Type": "application/json"}
        url = self.base_url + endpoint
        response = requests.get(url=url, json=payload, headers=headers, auth=self.auth, params=params)
        self.assert_status_code(response, expected_status_code, url)
        logger.debug(f"Sent GET REQUEST '{req_topic}' API response: {response.json()}")
        return response.json()

    def put(self, endpoint, req_topic, payload, headers=None, expected_status_code=200):
        if not headers:
            headers = {"Content-Type": "application/json"}
        url = self.base_url + endpoint
        response = requests.put(url=url, json=payload, headers=headers, auth=self.auth)
        self.assert_status_code(response, expected_status_code, url)
        logger.debug(f"PUT '{req_topic}' API response: {response.json()}")
        return response.json()
