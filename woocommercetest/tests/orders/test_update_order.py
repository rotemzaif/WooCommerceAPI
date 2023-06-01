import pdb
import pytest
import logging as logger
from woocommercetest.src.modules.ordersModule import Orders
from woocommercetest.src.utilities.genericUtilities import generate_random_string

pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.parametrize("new_status", [
    pytest.param('cancelled', marks=[pytest.mark.tcid55, pytest.mark.smoke]),
    pytest.param('completed', marks=pytest.mark.tcid56),
    pytest.param('on-hold', marks=pytest.mark.tcid57)
])
def test_update_order_status(new_status):
    logger.info(f"TEST: Update existing order's with new status: {new_status}")
    ord_obj = Orders()
    # create an order
    order_rs = ord_obj.create_order()
    cur_status = order_rs['status']
    assert cur_status != new_status, f"Current status of order is already '{new_status}'. Unable to run test"
    order_id = order_rs['id']
    # update order status
    payload = {"status": new_status}
    ord_obj.call_update_order(order_id, payload)
    # get the new order and verify its status was updated
    retrieve_new_ord = ord_obj.call_retrieve_order(order_id)
    assert retrieve_new_ord['status'] == new_status, f"Updated order status to '{new_status}' but order status is still '{retrieve_new_ord['status']}'"


@pytest.mark.tcid58
def test_update_order_invalid_status():
    logger.info("TEST: Update existing order's with non existing status")
    ord_obj = Orders()
    # create an order
    order_rs = ord_obj.create_order()
    new_status = generate_random_string()
    order_id = order_rs['id']
    # update order status
    payload = {"status": new_status}
    ord_update_rs = ord_obj.call_update_order(order_id, payload, expected_status_code=400)
    assert ord_update_rs['code'] == "rest_invalid_param", f"Unexpected Order update response code. Expected response code: 'rest_invalid_param' but got: {ord_update_rs['code']}"
    assert ord_update_rs['message'] == "Invalid parameter(s): status", f"Unexpected Order update response message. Expected response message: 'Invalid parameter(s): status' " \
                                                                       f"but got: {ord_update_rs['message']}"


@pytest.mark.tcid59
def test_update_order_customer_note():
    logger.info(f"TEST: Update existing order's 'customer notes' field")
    ord_obj = Orders()
    # create an order
    order_rs = ord_obj.create_order()
    cur_order_cust_notes = order_rs['customer_note']
    new_cust_notes = generate_random_string(length=40, prefix='customer_note')
    cust_notes = cur_order_cust_notes + ';' + new_cust_notes if cur_order_cust_notes else new_cust_notes
    payload = {"customer_note": cust_notes}
    order_id = order_rs['id']
    ord_obj.call_update_order(order_id, payload)
    retrieve_ord_rs = ord_obj.call_retrieve_order(order_id)
    assert retrieve_ord_rs["customer_note"] == cust_notes, f"Updated order {order_id} with 'customer notes' but notes were not added. Notes updated: {new_cust_notes}, Actual order " \
    f"'customer notes': {retrieve_ord_rs['customer_note']}"


