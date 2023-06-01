from woocommercetest.src.utilities.genericUtilities import generate_random_email_and_password
from woocommercetest.src.utilities.requestsUtility import RequestUtility


class Customers(object):
    def __init__(self):
        self.request_utility = RequestUtility()

    def create_customer(self, email=None, password=None, expected_status_code=201, **kwargs):
        if not email:
            email = generate_random_email_and_password()['email']
        if not password:
            password = 'Password1'
        payload = {'email': email, 'password': password}
        payload.update(kwargs)
        user_json = self.request_utility.post('customers', 'Create customer', payload=payload, expected_status_code=expected_status_code)
        return user_json

    def get_all_customers(self, params):
        return self.request_utility.get('customers', 'Get All customers', params=params)