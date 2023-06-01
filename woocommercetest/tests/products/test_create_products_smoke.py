import pytest
from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.productsModule import Products
from woocommercetest.src.utilities.genericUtilities import generate_random_string
import logging as logger

pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid26
def test_create_one_simple_product():
    logger.info("TEST: Create one simple product")

    # generate product data
    payload = {
        "name": generate_random_string(20),
        "type": "simple",
        "regular_price": "10.99"
    }

    # make a call
    rs_create_product = Products().create_product(payload)

    # verify response is not empty
    assert rs_create_product, f"ERROR: Create a simple product response is empty"

    # verify new product details
    assert rs_create_product["name"] == payload["name"], f"ERROR: Create product response name doesn't match payload name.\n" \
    f"Expected name: {payload['name']}\nActual name: {rs_create_product['name']}"

    assert rs_create_product["type"] == payload["type"], f"ERROR: Create product response type doesn't match payload name.\n" \
    f"Expected name: {payload['type']}\nActual name: {rs_create_product['type']}"

    assert rs_create_product["regular_price"] == payload["regular_price"], f"ERROR: Create product response price doesn't match payload name.\n" \
    f"Expected name: {payload['regular_price']}\nActual name: {rs_create_product['regular_price']}"

    # verify product was added to db
    prod_from_db = ProductsDAO().get_product_by_id_from_db(rs_create_product["id"])[0]
    assert prod_from_db, f"ERROR: Product was not added to db."

    assert prod_from_db["post_title"] == rs_create_product['name'], f"ERROR: Create Product, name in db ('post_title') doesn't match " \
    f"name in api.\nDB: {prod_from_db['post_title']}\nAPI: {rs_create_product['name']}"
