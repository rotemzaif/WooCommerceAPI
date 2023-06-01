import logging as logger
import random
import pytest
from woocommercetest.src.modules.couponModule import Coupons
from woocommercetest.src.modules.ordersModule import Orders
from woocommercetest.src.modules.productsModule import Products


@pytest.fixture
def orders_setup():
    def _orders_setup(qty=1):
        rand_products = Products().get_all_products({"type": "simple"})
        rand_products = random.sample(rand_products, qty)
        return rand_products
    return _orders_setup


@pytest.mark.orders
@pytest.mark.tcid60
def test_apply_valid_coupon_to_order(orders_setup):
    """
    This test validated that when applying an %x coupon to an order, the order 'total' amount is reduced by x percen
    """
    logger.info("TEST: apply a valid coupon to order and verify order total amount")
    product = orders_setup()[0]
    coupon = Coupons().get_generic_coupon_with_percentage("50")
    order_payload_addition = {
        "line_items": [{"product_id": product['id'], "quantity": 1}],
        "coupon_lines": [{"code": coupon['code']}],
        "shipping_lines": [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]
    }
    flat_rate_val = float(order_payload_addition['shipping_lines'][0]['total'])
    expected_total = float(product['price']) * order_payload_addition['line_items'][0]['quantity'] * float(coupon['amount']) / 100
    expected_total = "{:.2f}".format(expected_total + flat_rate_val)
    order_rs = Orders().create_order(additional_args=order_payload_addition)
    assert order_rs['total'] == expected_total, f"Unexpected order 'total' amount after applying a {coupon['amount']}% discount coupon. Expected: {expected_total} " \
                                                f"but got {order_rs['total']}."





    # make an order with an x% discount coupon
    # verify order total amount is reduced by x%
    # coupon_obj = Coupons()
    # product_obj =
    # order_obj = Orders()
    # discount_per = "50.00"






