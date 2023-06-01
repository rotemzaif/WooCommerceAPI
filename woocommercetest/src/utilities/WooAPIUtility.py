import os
from woocommerce import API

import logging as logger

from woocommercetest.src.configs.hosts_config import WOO_API_HOSTS
from woocommercetest.src.utilities.credentialsUtility import CredentialsUtility


class WooAPIUtility(object):

    def __init__(self):
        wc_cred = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = WOO_API_HOSTS[self.env]
        self.wcapi = API(
            url=self.base_url,
            consumer_key=wc_cred['wc_key'],
            consumer_secret=wc_cred['wc_secret'],
            version="wc/v3"
        )

    @staticmethod
    def assert_status_code(response, expected_status_code, url):
        assert response.status_code == expected_status_code, f"Wrong status code." \
        f"Expected {expected_status_code}, Actual: {response.status_code}," \
        f"URL: {url}, Response json: {response.json()}"

    def get(self, wc_endpoint, req_topic, params=None, expected_status_code=200):
        response = self.wcapi.get(wc_endpoint, params=params)
        self.assert_status_code(response, expected_status_code, wc_endpoint)
        logger.debug(f"GET '{req_topic}' API response: {response.json()}")
        return response.json()

    def post(self, wc_endpoint, req_topic, payload=None, expected_status_code=200):
        response = self.wcapi.post(wc_endpoint, data=payload)
        self.assert_status_code(response, expected_status_code, wc_endpoint)
        logger.debug(f"POST '{req_topic}' API response: {response.json()}")
        return response.json()

    def put(self, wc_endpoint, req_topic, item_id, payload, expected_status_code=200):
        response = self.wcapi.put(wc_endpoint, data=payload)
        self.assert_status_code(response, expected_status_code, wc_endpoint)
        logger.debug(f"PUT '{req_topic}' API response: {response.json()}")
        return response.json()

    def delete(self, wc_endpoint, req_topic, force=False, expected_status_code=200):
        response = self.wcapi.delete(wc_endpoint, params={"force": force})
        self.assert_status_code(response, expected_status_code, wc_endpoint)
        logger.debug(f"{req_topic}' API response: {response.json()}")
        return response.json()



if __name__ == '__main__':
    import os
    cur_file_dir = os.path.dirname(os.path.realpath(__file__))
    print(f"current directory path is: {cur_file_dir}")
    # obj = WooAPIUtility()
    # rs_api = obj.get('products', 'list all products')
    # from pprint import pprint as pp
    # pp(rs_api)
