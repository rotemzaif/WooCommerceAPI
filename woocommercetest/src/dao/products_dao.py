import random
from woocommercetest.src.utilities.dbUtility import DBUtility
import logging as logger


class ProductsDAO(object):
    def __init__(self):
        self.db_obj = DBUtility()
        self.db_name = self.db_obj.database

    def get_all_products_including_variation_products(self):
        """
        get all products from db with 'post type' that includes 'product' (can be either 'product' or 'product_variation')
        Returns: a list of products (post type = 'product' or 'product_variation') sorted by product id ascending

        """
        sql = f"SELECT * FROM {self.db_name}.wp_posts WHERE post_type like 'product%' ORDER BY ID;"
        return self.db_obj.execute_query(sql)

    def get_all_products(self):
        """
        get all products from the db with 'post type' = 'product'
        Returns: a list of products (post type = 'product') sorted by product id ascending
        """

        sql = f"SELECT * FROM {self.db_name}.wp_posts WHERE post_type = 'product' ORDER BY ID;"
        return self.db_obj.execute_query(sql)

    def get_all_products_with_date_filter(self, filter_operator, after_date):
        """
        Get all products from db with 'post type' = 'product' before/after a given date
        Args:
            filter_operator: str - can be either '>' (after) or '<' (before)
            after_date: str - date in format '%Y-%m-%dT%H:%m:%S'

        Returns: a list of products (dicts) before/after a given date sorted by product id ascending

        """
        sql = f"SELECT * FROM {self.db_name}.wp_posts WHERE post_type = 'product' AND post_date {filter_operator} '{after_date}' ORDER BY ID;"
        return self.db_obj.execute_query(sql)

    def get_a_random_product_from_db(self, qty=1):
        """
        returns a randon product/s from the products list in db
        Args:
            qty: int, number of products to return
        Returns: a list of random products dicts
        """
        logger.debug("Getting random products from DB")
        all_products = self.get_all_products()  # getting a list of all products/records
        random_products = random.sample(all_products, int(qty))  # using random.sample to return a list of random products dicts
        logger.debug(f"Got random products from DB: {random_products}")
        return random_products

    def get_product_by_id_from_db(self, prod_id):
        """

        Args:
            prod_id: int, id of the product to return

        Returns: the product record with the given id

        """
        sql = f"SELECT * FROM {self.db_name}.wp_posts WHERE ID = {prod_id};"
        return self.db_obj.execute_query(sql)

    def get_random_product_without_sale_price(self, qty=1):
        """
        returns a list of product ids which do not have a sale price
        Args:
            qty: int, number of products to return

        Returns: list on ids (int)

        """
        logger.debug("Getting random products from DB that are not on 'sale'. I.E. products that don't have a 'sale price'")
        sql = f"SELECT * FROM {self.db_name}.wp_postmeta pm " \
              f"JOIN {self.db_name}.wp_posts p ON pm.post_id = p.ID " \
              f"WHERE p.post_type = 'product' AND pm.meta_key='_sale_price' AND pm.meta_value='';"
        products_without_sale_price = self.db_obj.execute_query(sql)
        if not products_without_sale_price:
            logger.debug("Did not find products without 'sale_price' value empty")
            return []
        random_products = random.sample(products_without_sale_price, int(qty))
        logger.debug(f"Got random products with 'sale price' from DB: {random_products}")
        return random_products

    def get_random_product_with_sale_price(self, qty=1):
        logger.debug("Getting random products from DB that are on 'sale'. I.E products that have a 'sale price'")
        sql = f"SELECT pm.post_id as id, pm.meta_value as sale_price, p.post_title FROM {self.db_name}.wp_postmeta pm " \
              f"JOIN {self.db_name}.wp_posts p ON pm.post_id = p.ID " \
              f"WHERE p.post_type = 'product' AND pm.meta_key='_sale_price' AND pm.meta_value<>'';"
        products_on_sale = self.db_obj.execute_query(sql)
        if products_on_sale:
            random_products = random.sample(products_on_sale, int(qty))
            logger.debug(f"Got random products that have 'sale price' ('sale price' > 0): {random_products}")
            return random_products
        else:
            logger.debug("Did not find any products that are on 'sale' ('sale price' = 0).")
            return products_on_sale
