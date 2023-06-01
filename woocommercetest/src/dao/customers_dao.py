import random
from woocommercetest.src.utilities.dbUtility import DBUtility


class CustomerDAO(object):

    def __init__(self):
        self.db_obj = DBUtility()
        self.db_name = self.db_obj.database

    def get_customer_by_email(self, email):
        sql = f"SELECT * FROM {self.db_name}.wp_users WHERE user_email = '{email}';"
        return self.db_obj.execute_query(sql)

    def get_all_customers(self):
        sql = f"SELECT * FROM {self.db_name}.wp_users WHERE ID <> 1;"
        return self.db_obj.execute_query(sql)

    def get_random_customer_from_db(self, qty=1):
        '''
        returns a randon customer from the customers list in db
        Args:
            qty: int, number of customers to return
        Returns: a list of random customers

        '''
        total_customers = self.get_all_customers()  # getting a list of all customers/records
        return random.sample(total_customers, int(qty))  # using random.sample to return a list of random customers

