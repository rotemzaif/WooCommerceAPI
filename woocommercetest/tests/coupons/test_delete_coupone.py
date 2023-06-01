import pdb

import pytest

from woocommercetest.src.modules.couponModule import Coupons
from woocommercetest.src.utilities.genericUtilities import generate_random_coupon_code


@pytest.mark.tcid42
def test_delete_coupon_smoke():
    coupon_obj = Coupons()
    discount_pct = "30"
    payload = {
        "code": generate_random_coupon_code(discount_pct, length=5),
        "amount": discount_pct
    }
    coupon_rs = coupon_obj.call_create_coupons(payload=payload)
    del_coup_rs = coupon_obj.call_delete_coupon(coupon_rs['id'], force=True)
    assert del_coup_rs['id'] == coupon_rs['id'], f"DELETE coupon response: coupon id doesn't match requested coupon id. Requested coupon id: {coupon_rs['id']} but got: {del_coup_rs['id']}"

    ret_coupon = coupon_obj.call_retrieve_coupon(coupon_rs['id'], expected_status_code=404)
    assert ret_coupon['message'] == "Invalid ID.", f"Unexpected RETRIEVE coupon response message. Expected: 'Invalid ID.' but got: 'ret_coupon['message']'"
