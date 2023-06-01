import random

import pytest
import logging as logger
import pdb

from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.productsModule import Products
from woocommercetest.src.utilities.genericUtilities import generate_random_string


pytestmark = [pytest.mark.products, pytest.mark.product_update, pytest.mark.regression]

@pytest.mark.tcid61
def test_update_regular_price_should_update_price():
    logger.info("TEST: Verify Update product 'regular_price' is updating 'price' field")
    prod_obj = Products()
    prod_db_obj = ProductsDAO()
    rand_products_without_sale_price = prod_db_obj.get_random_product_without_sale_price()
    if rand_products_without_sale_price:
        product_id = rand_products_without_sale_price[0]['post_id']
    else:  # if there are no products with an empty 'sale price' value --> get a random product and update its 'sale price' to an empty string
        rand_product = prod_db_obj.get_a_random_product_from_db()[0]
        product_id = rand_product['ID']
        payload = {"sale_price": ''}
        prod_obj.call_update_product(product_id, payload)

    # update product 'regular price'
    new_reg_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
    payload = {"regular_price": new_reg_price}
    prod_update_rs = prod_obj.call_update_product(product_id, payload)

    # verify 'regular price' & 'price' value in response
    assert prod_update_rs['regular_price'] == new_reg_price, f"ERROR: Unexpected 'regular_price' value in product update api response. Expected: {new_reg_price} " \
    f"but got: {prod_update_rs['regular_price']}"
    assert prod_update_rs['price'] == new_reg_price, f"ERROR: Unexpected 'price' value in product update api response. Expected: {new_reg_price} " \
    f"but got: {prod_update_rs['price']}"

    # retrieve product
    ret_product = prod_obj.call_retrieve_product(product_id)
    assert ret_product['regular_price'] == new_reg_price, f"ERROR: Unexpected 'regular_price' value in product update response. Expected: {new_reg_price} " \
    f"but got: {prod_update_rs['regular_price']}"
    assert ret_product['price'] == new_reg_price, f"ERROR: Update product api call: updating the 'regular_price' did not update the 'price' field. " \
    f"Expected 'price': {new_reg_price}, Actua: {ret_product['price']}"


@pytest.mark.tcid63
@pytest.mark.tcid64
def test_update_on_sale_field_by_updating_sale_price():
    logger.info("TEST: Verify 'on_sale' field is 'true' when updating 'sale_price' field with a value > 0 and 'false' when updating 'sale_price' = '' ")
    prod_obj = Products()
    prod_db_obj = ProductsDAO()
    rand_products_without_sale_price = prod_db_obj.get_random_product_without_sale_price()
    if rand_products_without_sale_price:
        product_id = rand_products_without_sale_price[0]['post_id']
    else:  # if there are no products that are not on sale --> create a new product with 'sale_price' = ''
        payload = {
            "name": generate_random_string(),
            "type": "simple",
            "regular_price": str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
        }
        new_prod_rs = prod_obj.create_product(payload)
        product_id = new_prod_rs['id']
        assert new_prod_rs['sale_price'] == "", f"Newly created product has a 'sale_price' although was not given by the user. Product id: {product_id}"
    ret_product = prod_obj.call_retrieve_product(product_id)
    assert not ret_product['on_sale'], f"Tested product (id: {product_id} 'on sale' field is {ret_product['on_sale']} although its 'sale price' is empty. Cannot test with this product)"

    # tcid63
    sale_price = float(ret_product['regular_price']) * 0.75
    prod_obj.call_update_product(product_id, {"sale_price": str(sale_price)})
    product_after_update = prod_obj.call_retrieve_product(product_id)
    assert product_after_update['on_sale'], f"Product (id: {product_id}) 'on_sale' field was not set to 'true' although 'sale_price' field has a value"

    # tcid64
    prod_obj.call_update_product(product_id, {"sale_price": ''})
    product_after_update = prod_obj.call_retrieve_product(product_id)
    assert not product_after_update['on_sale'], f"Product (id: {product_id}) 'on_sale' field was not set to 'false' after updating 'sale_price' with an empty value"


@pytest.mark.tcid65
def test_update_sale_price_and_verify_field_is_updated():
    logger.info("TEST: Update 'sale_price' field with valid sale price and verify 'sale_price' value is updated accordingly")
    prod_obj = Products()
    prod_db_obj = ProductsDAO()
    rand_products_on_sale = prod_db_obj.get_random_product_with_sale_price()
    product = prod_obj.call_retrieve_product(rand_products_on_sale[0]['id']) if rand_products_on_sale else create_product_with_sale_price(prod_obj)
    product_id = product['id']
    product_sale_price = product['sale_price']

    # update product 'sale price'
    new_sale_price = str(float(product_sale_price) * 0.9)
    payload = {'sale_price': new_sale_price}
    prod_update_rs = prod_obj.call_update_product(product_id, payload)

    # verify sale price in response
    assert prod_update_rs['sale_price'] == new_sale_price, f"New 'sale price' is not displayed in the product UPDATE call response. Expected {new_sale_price} but got " \
                                                           f"{prod_update_rs['sale_price']}. Product id: {product_id}"

    # retrieve product
    ret_product = prod_obj.call_retrieve_product(product_id)
    assert ret_product['sale_price'] == new_sale_price, f"New 'sale price' is not displayed in the Retrieve Product call response. Expected {new_sale_price} but got " \
                                                           f"{prod_update_rs['sale_price']}. Product id: {product_id}"


@pytest.mark.tcid62
def test_update_sale_price_with_higher_price_than_regular_price():
    logger.info("TEST: Update product 'sale_price' field with a price higher than the regular price and verify that the sale price changes to '' and price value is updated to "
                "'regular price'")
    prod_obj = Products()
    prod_db_obj = ProductsDAO()
    # select a random product
    rand_products_on_sale = prod_db_obj.get_random_product_with_sale_price()
    product = prod_obj.call_retrieve_product(rand_products_on_sale[0]['id']) if rand_products_on_sale else create_product_with_sale_price(prod_obj)
    product_id = product['id']
    product_regular_price = product['regular_price']

    # update product 'sale price'
    new_sale_price = str(float(product_regular_price) * 1.2)
    payload = {'sale_price': new_sale_price}
    prod_update_rs = prod_obj.call_update_product(product_id, payload)
    # verify 'sale price' and 'regular price' in the update response
    assert prod_update_rs['sale_price'] == '', f"Updated Product 'sale price' with a higher price than 'regular price', but 'sale price' value was not updated to '' (empty value) in " \
    f" the UPDATE call response. Product: {prod_update_rs}"
    assert prod_update_rs['price'] == prod_update_rs['regular_price'], f"Updated Product 'sale price' with a higher price than 'regular price', but 'price' was not updated with " \
    f"'regular price' in the UPDATE call response. Product: \n{prod_update_rs}"

    # retrieve product
    ret_product = prod_obj.call_retrieve_product(product_id)
    assert ret_product['sale_price'] == '', f"Updated Product 'sale price' with a higher price than 'regular price', but got 'sale price': {ret_product['sale_price']} in " \
    f" the RETRIEVE PRODUCT call response. Product: {ret_product}"
    assert ret_product['price'] == ret_product['regular_price'], f"Unexpected 'price' value in RETRIEVE PRODUCT call after updating 'sale price' with a higher value than " \
    f"the 'regular price'. Expected: {ret_product['regular_price']} but got:  {ret_product['price']}"


''' assistance methods '''


def create_product_with_sale_price(product_obj):
    regular_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
    sale_price = float(regular_price) * 0.75
    sale_price = str("{:.2f}".format(sale_price))
    payload = {
        "name": generate_random_string(),
        "type": "simple",
        "regular_price": regular_price,
        "sale_price": sale_price
    }
    new_prod_rs = product_obj.create_product(payload)
    assert new_prod_rs['sale_price'] == sale_price, f"Newly created product (id: {new_prod_rs['id']}) has unexpected 'sale price'. expected {sale_price} but got " \
                                                    f"{new_prod_rs['sale_price']}. "
    return new_prod_rs










