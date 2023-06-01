import logging as logger
import pytest

from woocommercetest.src.dao.customers_dao import CustomerDAO
from woocommercetest.src.modules.customerModule import Customers


@pytest.mark.customers
@pytest.mark.tcid30
def test_get_all_customers():
    logger.info("TEST: Get all customers")
    # make a call to get all customers
    cust_obj = Customers()
    params = {'per_page': 100}
    cust_list = cust_obj.get_all_customers(params=params)
    # assert received customer list is not empty
    assert cust_list, f"Response of list all Customers is empty"

    # assert number of customers in api is similar to number of customers in database
    db_cust_list = CustomerDAO().get_all_customers()
    assert len(cust_list) == len(db_cust_list), f"ERROR: Number of customers from API ({len(cust_list)}) is different from number of customers in database ({len(db_cust_list)})"
