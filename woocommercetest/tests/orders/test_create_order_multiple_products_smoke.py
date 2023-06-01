import pytest
from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.ordersModule import Orders
import logging as logger

@pytest.fixture
def orders_setup():
    def _orders_setup(qty=1):
        rand_products = ProductsDAO().get_a_random_product_from_db(qty)
        product_ids = list(map(lambda x: x['ID'], rand_products))
        return product_ids
    return _orders_setup


# @pytest.mark.orders
@pytest.mark.tcid50
def test_create_paid_order_multiple_products_guest_user(orders_setup):
    logger.info("TEST: Create paid order with multiple products and guest user")
    rand_products = orders_setup(2)
    payload = {
        "line_items": [
            {
                "product_id": rand_products[0],
                "quantity": 2
            },
            {
                "product_id": rand_products[1],
                "quantity": 1
            }
        ]
    }
    order_obj = Orders()
    ord_resp = order_obj.create_order(payload)
    customer_id = 0
    order_obj.verify_order_response(ord_resp, customer_id, payload['line_items'])
    order_obj.verify_order_in_db(ord_resp['id'], ord_resp['line_items'])