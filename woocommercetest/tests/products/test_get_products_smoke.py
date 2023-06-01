import pytest
import logging as logger

from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.productsModule import Products

pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid24
def test_get_all_products():
    logger.info("TEST: List all products")

    # make a call to get all products
    prod_obj = Products()
    params = {'per_page': 100, 'orderby': 'id', 'order': 'asc'}
    products_list = prod_obj.get_all_products(params)

    # assert products list is not empty
    assert products_list, f"'get all products' endpoint returns an empty Products list"

    # assert number of products from api is identical to the number of products from the db
    db_prod_list = ProductsDAO().get_all_products()
    assert len(products_list) == len(
        db_prod_list), f"ERROR: number of products from api response ({len(products_list)}) " \
                       f"does not match number of products from db {len(db_prod_list)}"

@pytest.mark.tcid25
def test_get_product_by_id():
    logger.info("TEST: Get a product by id")
    # get a random product (test data) from db
    rand_prod = ProductsDAO().get_a_random_product_from_db()
    prod_id = rand_prod[0]['ID']

    # make a call to get a product by id
    prod_obj = Products()
    prod_api_info = prod_obj.call_retrieve_product(prod_id)

    # verify retrieved product response is not empty
    assert prod_api_info, f"ERROR: 'Retrieve a Product' endpoint returns nothing for product id {rand_prod['ID']}"

    # verify retrieved product id is identical to the requested id
    assert prod_api_info['id'] == prod_id, f"ERROR: retrieved product id doesn't match the requested product.\n" \
                                                   f"Expected ID: {prod_id}" \
                                                   f"\nAPI product id: {prod_api_info['id']}"


@pytest.mark.tcid27
def test_get_product_by_id_fail_for_nonexisting_product():
    logger.info("TEST: Get product product with non-existing product id")
    # get a product id that doesn't exist in the db
    # getting all products from db including variation products in ascending order
    last_prod = ProductsDAO().get_all_products_including_variation_products()[-1]
    non_existing_prod_id = last_prod['ID'] + 1

    # make a call
    prod_obj = Products()
    rs_prod = prod_obj.call_retrieve_product(non_existing_prod_id, expected_status_code=404)

    # verify response code
    expected_rs_api_code = "woocommerce_rest_product_invalid_id"
    assert rs_prod['code'] == expected_rs_api_code, f"ERROR: incorrect response code when retrieving a product that doesn't exist.\n" \
                                                    f"Expected code: {expected_rs_api_code}\n" \
                                                    f"Actual code: {rs_prod['code']}"
    # verify response message
    expected_message = "Invalid ID."
    assert rs_prod['message'] == expected_message, f"ERROR: incorrect response error message when retrieving a product that doesn't exist.\n" \
                                                f"Expected message: {expected_message}\n" \
                                                f"Actual message: {rs_prod['message']}"


