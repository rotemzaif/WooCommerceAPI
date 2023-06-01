import pdb

from woocommercetest.src.utilities.requestsUtility import RequestUtility
import logging as logger


class Products(object):
    def __init__(self):
        self.request_obj = RequestUtility()

    def get_all_products(self, params=None):
        """
        get all products from all pages
        Args:
            params: a dict of params to be passed to the request

        Returns: a list of product dictionaries (each dictionary represents a product) based on request params

        """
        max_pages = 1000
        all_products = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products per page: {i}")
            if not params:
                params = {}
            if 'per_page' not in params.keys():
                params['per_page'] = 100
            # add the current page number to the call
            params['page'] = i
            response = self.request_obj.get('products', 'List All Products', params=params)
            if not response:  # if the response is empty then there are no more products --> stopping the loop
                break
            all_products.extend(response)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")
        return all_products

    def call_retrieve_product(self, prod_id, expected_status_code=200):
        """
        get a product by its id
        Args:
            prod_id: product id to be returned
            expected_status_code: request call expected status call. Option to insert status_code != 200 for testing negative scenarios
        Returns: GET request response json
        """
        return self.request_obj.get(f"products/{prod_id}", "Get Product By ID", expected_status_code=expected_status_code)

    def create_product(self, payload, expected_status_code=201):
        """
        create a new product
        Args:
            payload: a dictionary with product attributes to be created
            expected_status_code: request call expected status call. Option to insert status_code!= 201 for testing negative scenarios
        Returns: POST request response json
        """
        return self.request_obj.post('products', 'Create Product', payload=payload, expected_status_code=expected_status_code)

    def call_update_product(self, prod_id, payload, expected_status_code=200):
        """
        This method updates an existing product
        Args:
            prod_id: int - product id to be updated
            payload: dict - product properties to be updated
            expected_status_code: int - request call expected status call

        Returns: PUT request response json

        """
        if not payload:
            raise Exception("Payload is empty. Cannot make a PUT  request with an empty payload.")
        return self.request_obj.put(f'products/{prod_id}', 'Update product', payload=payload, expected_status_code=expected_status_code)



