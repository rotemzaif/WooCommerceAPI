import pytest
import logging as logger
from datetime import datetime, timedelta
from woocommercetest.src.dao.products_dao import ProductsDAO
from woocommercetest.src.modules.productsModule import Products


@pytest.mark.products
@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):
        logger.info("TEST: List all products with filter 'after'")

        # create request parameters payload
        x_days_from_today = 300
        after_created_date = (datetime.now() - timedelta(days=x_days_from_today)).strftime('%Y-%m-%dT%H:%m:%S')
        # using params 'order by'='id' and 'order'='asc' to get an ordered list
        params = {'orderby': 'id', 'order': 'asc', 'after': after_created_date}

        # make the call
        rs_prod_list = Products().get_all_products(params)

        # get data from db
        db_products_list = ProductsDAO().get_all_products_with_date_filter('>', after_created_date)

        # verify the response
        assert len(rs_prod_list) == len(db_products_list), f"List products with filter 'after' returns unexpected number of products.\n" \
        f"Expected: {len(db_products_list)}\nActual: {len(rs_prod_list)}"

        # verify products id's in api list are the same as in db
        if len(rs_prod_list) > 0:
            ids_in_api = list(map(lambda x: x['id'], rs_prod_list))
            ids_in_db = list(map(lambda x: x['ID'], db_products_list))
            ids_diff = list(set(ids_in_api) - set(ids_in_db))
            assert not ids_diff, "ERROR: List products with filter 'after' - products ids in response mismatch in db"
