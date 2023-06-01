import logging as logger
import pdb
import random
import pytest
from woocommercetest.src.modules.couponModule import Coupons
from woocommercetest.src.utilities.genericUtilities import generate_random_coupon_code, generate_random_string

pytestmark = [pytest.mark.regression, pytest.mark.coupons]


@pytest.fixture(scope='module')
def my_setup():
    info = {'coupon_obj': Coupons()}
    return info


@pytest.mark.parametrize('discount_type',
                         [
                             pytest.param(None, marks=[pytest.mark.tcid37, pytest.mark.smoke]),
                             pytest.param('percent', marks=[pytest.mark.tcid37, pytest.mark.smoke]),
                             pytest.param('fixed_cart', marks=pytest.mark.tcid38),
                             pytest.param('fixed_product', marks=pytest.mark.tcid39)
                         ])
def test_create_coupon_with_discount_type(request, my_setup, discount_type):
    logger.info(f"TEST: creating a coupon with '{discount_type}' discount type and verifying it is created with the correct details.")
    coupon = my_setup['coupon_obj']
    # one of the tests is to send an empty discount type and verify that the default is used in this case.
    expected_discount_type = discount_type if discount_type else 'fixed_cart'
    discount_pct = str(random.randint(50, 90)) + ".00"
    test_id = get_test_mark_name(request.node.own_markers)
    coupon_code = generate_random_coupon_code(discount_pct, prefix=test_id, length=5)
    payload = {
        "code": coupon_code,
        "amount": discount_pct
    }
    if discount_type:
        payload['discount_type'] = discount_type
    coupon_rs = coupon.call_create_coupons(payload=payload)
    # verify CREATE coupon response
    assert coupon_rs['code'] == coupon_code, f"Create Coupon response has wrong code. Expected: '{coupon_code}' but got '{coupon_rs['code']}'"
    assert coupon_rs['amount'] == discount_pct, f"Create Coupon response has wrong amount. Expected: '{discount_pct}' but got '{coupon_rs['amount']}'"
    assert coupon_rs['discount_type'] == expected_discount_type, f"Create Coupon response has wrong discount type. Expected: '{discount_type}' but got '{coupon_rs['discount_type']}'"
    # verify RETRIEVE coupon response
    coupon_id = coupon_rs['id']
    ret_coupon_rs = coupon.call_retrieve_coupon(coupon_id)
    assert ret_coupon_rs['code'] == coupon_code, f"Retrieve Coupon response has wrong code. Expected: '{coupon_code}' but got '{ret_coupon_rs['code']}'"
    assert ret_coupon_rs['amount'] == discount_pct, f"Retrieve Coupon response has wrong amount. Expected: '{discount_pct}' but got '{ret_coupon_rs['amount']}'"
    assert ret_coupon_rs['discount_type'] == expected_discount_type, f"Retrieve Coupon response has wrong discount type. Expected: '{discount_type}' but got '{ret_coupon_rs['discount_type']}'"


@pytest.mark.tcid40
def test_create_coupon_with_invalid_discount_type(my_setup):
    """
    This test creates a coupon with an invalid discount type by generating a random string and verifies that the call fails with
    correct error message
    """
    logger.info(f"TEST: creating a coupon with invalid 'discount type'")
    coupon_obj = my_setup['coupon_obj']
    discount_pct = str(random.randint(50, 90)) + ".00"
    payload = {
        "code": generate_random_coupon_code(discount_pct, "tcid40", length=5),
        "amount": discount_pct,
        "discount_type": generate_random_string()
    }
    coupon_rs = coupon_obj.call_create_coupons(payload=payload, expected_status_code=400)
    expected_res_code = "rest_invalid_param"
    assert coupon_rs['code'] == expected_res_code, f"Unexpected Create Coupon response code. Expected: '{expected_res_code}' but got " \
                                                   f"'{coupon_rs['code']}'"
    expected_err_msg = "Invalid parameter(s): discount_type"
    assert coupon_rs['message'] == expected_err_msg, f"Unexpected Create Coupon call failure message. " \
                                                     f"Expected message: '{expected_err_msg}' but got '{coupon_rs['message']}'"
    assert 'discount_type' in coupon_rs['data']['params'], "'discount_type' is not listed under data/params in the Create Coupon failure response "
    assert 'discount_type' in coupon_rs['data']['details'], "'discount_type' is not listed under data/details in the Create Coupon failure response "
    expected_details_code = "rest_not_in_enum"
    actual_details_code = coupon_rs['data']['details']['discount_type']['code']
    assert actual_details_code == expected_details_code, f"Unexpected Create Coupon call failure data/details/discount_type code. " \
    f"Expected: '{expected_details_code}' but got: '{actual_details_code}'"
    expected_details_msg = "discount_type is not one of percent, fixed_cart, and fixed_product."
    actual_details_msg = coupon_rs['data']['details']['discount_type']['message']
    assert actual_details_msg == expected_details_msg, f"Unexpected Create Coupon call failure data/details/discount_type message. " \
                                                       f"Expected: '{expected_details_msg}' but got: '{actual_details_msg}'"


@pytest.mark.tcid41
def test_create_coupon_with_existing_code(my_setup):
    """
    This test creates a new Coupon with an existing coupon name/code and verifies that the call fails with a relevant error message
    """
    logger.info(f"TEST: creating a coupon with existing coupon code")
    coupon_obj = my_setup['coupon_obj']
    rand_coupon = random.choice(coupon_obj.call_list_all_coupons())
    payload = {
        "code": rand_coupon['code'],
        "amount": "30"
    }
    coupon_rs = coupon_obj.call_create_coupons(payload=payload, expected_status_code=400)
    expected_rs_code = "woocommerce_rest_coupon_code_already_exists"
    assert coupon_rs['code'] == expected_rs_code, f"Unexpected code in response after Create coupon with existing code. Expected: " \
                                                  f"'{expected_rs_code}' but got: '{coupon_rs['code']}'"
    expected_rs_msg = "The coupon code already exists"
    assert coupon_rs['message'] == expected_rs_msg, f"Unexpected message in response after Create coupon with existing code. Expected: " \
                                                    f"'{expected_rs_msg}' but got: '{coupon_rs['message']}'"


def get_test_mark_name(test_markers):
    markers_name = list(map(lambda x: x.name, test_markers))
    for m in markers_name:
        if 'tc' in m:
            return m



