import pytest
import logging as logger

from woocommercetest.src.dao.customers_dao import CustomerDAO
from woocommercetest.src.modules.customerModule import Customers
from woocommercetest.src.utilities.genericUtilities import generate_random_email_and_password


@pytest.mark.customers
@pytest.mark.tcid29
def test_create_customer_only_email_password():
    logger.info("TEST: Create new customer with email and password only")
    rand_info = generate_random_email_and_password()
    email = rand_info['email']
    password = rand_info['password']

    # make the request/call
    cust_obj = Customers()
    cust_api_info = cust_obj.create_customer(email=email, password=password)
    assert cust_api_info['email'] == email, f"Error: Create customer api returns wrong email: {cust_api_info['email']}"
    assert cust_api_info['first_name'] == '', f"Error: Create customer api returned value for first_name: {cust_api_info['first_name']} but should be empty"

    # verify customer was created in db
    db_res = CustomerDAO().get_customer_by_email(email)
    assert db_res, f"User with email {email} was not inserted to the DB"
    assert len(db_res) == 1, f"User with email {email} has more than one record in the db: {db_res}"
    cust_db_info = db_res[0]
    assert cust_api_info['id'] == cust_db_info['ID'], f"Error: user 'id' in db doesn't match created user id.\nCreated user: {cust_api_info}" \
    f"\nDB user info: {cust_db_info}"

@pytest.mark.customers
@pytest.mark.tcid47
def test_create_customer_fail_for_existing_email():
    logger.info("TEST: Create new customer with existing email in the db")
    # get a randon user from the db
    existing_cust = CustomerDAO().get_random_customer_from_db()
    existing_email = existing_cust[0]['user_email']

    # call the api
    cust_obj = Customers()
    cust_api_info = cust_obj.create_customer(email=existing_email, expected_status_code=400)

    # verify response code
    expected_code = "registration-error-email-exists"
    assert cust_api_info['code'] == expected_code, f"Error: incorrect POST api response code.\nExpected: " \
                                                   f"{expected_code}\nActual: {cust_api_info['code']}"

    # verify response data.status
    assert cust_api_info['data'][
               'status'] == 400, f"Error: POST api response body 'status' doesn't match request status_code." \
                                 f"\nExpected: 400" \
                                 f"\nActual: {cust_api_info['data']['status']} "

    # verify response message
    expected_msg = "An account is already registered with your email address. <a href=\"#\" class=\"showlogin\">Please log in.</a>"
    assert cust_api_info[
               'message'] == expected_msg, f"Error: Incorrect Create customer with existing user error 'message'\n" \
                                           f"Expected message: {expected_msg}\n" \
                                           f"Actual message: {cust_api_info['message']}"




