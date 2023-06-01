import pytest
from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.customerModule import Customers
from woocommercetest.src.modules.ordersModule import Orders
import logging as logger


@pytest.fixture(scope="module")
def orders_setup():
    # get a random product from the db
    rand_product = ProductsDAO().get_a_random_product_from_db(1)[0]
    product_id = rand_product['ID']
    order_obj = Orders()
    info = {
        "product_id": product_id,
        "order_obj": order_obj
    }
    return info


@pytest.mark.smoke
@pytest.mark.orders
@pytest.mark.tcid48
def test_create_paid_order_single_product_guest_user(orders_setup):
    logger.info("TEST: Create paid order with guest user")
    order_obj = orders_setup['order_obj']
    product_id = orders_setup['product_id']
    # create order payload
    payload = {
        "line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ]}

    # make the call
    ord_resp = order_obj.create_order(payload)
    customer_id = 0  # since guest user id is 0

    # verify order api response and db recording
    order_obj.verify_order_response(ord_resp, customer_id, payload['line_items'])
    order_obj.verify_order_in_db(ord_resp['id'], ord_resp['line_items'])

@pytest.mark.smoke
@pytest.mark.orders
@pytest.mark.tcid49
def test_create_paid_order_single_product_new_customer(orders_setup):
    logger.info("TEST: Create paid order with new customer")
    # create new customer
    cust_info = Customers().create_customer()
    customer_id = cust_info['id']

    order_obj = orders_setup['order_obj']
    product_id = orders_setup['product_id']
    # create order payload
    payload = {
        "line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ],
        "customer_id": customer_id
    }

    # make order call
    ord_resp = order_obj.create_order(payload)

    # verify order api response and db recording
    order_obj.verify_order_response(ord_resp, customer_id, payload['line_items'])
    order_obj.verify_order_in_db(ord_resp['id'], ord_resp['line_items'])

