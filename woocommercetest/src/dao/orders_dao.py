from woocommercetest.src.utilities.dbUtility import DBUtility


class OrdersDAO(object):
    def __init__(self):
        self.db_obj = DBUtility()
        self.db_name = self.db_obj.database

    def get_order_lines_by_order_id(self, order_id):
        db_name = self.db_obj.database
        sql = f"SELECT * FROM {self.db_name}.wp_woocommerce_order_items WHERE order_id={order_id};"
        return self.db_obj.execute_query(sql)

    def get_order_items_details(self, line_items_ids):
        """
        This method executes a query to get metadata for all line items ids given
        Args:
            line_items_ids: list of line items ids

        Returns: dict - key = line items id, value = dict (key = meta key, value = meta value

        """
        line_items_ids_str = ",".join(str(x) for x in line_items_ids)
        sql = f"SELECT * FROM {self.db_name}.wp_woocommerce_order_itemmeta WHERE order_item_id in ({line_items_ids_str});"
        rs_sql = self.db_obj.execute_query(sql)
        order_items_details_dict = {k: {v['meta_key']: v['meta_value'] for v in rs_sql if v['order_item_id'] == k} for k in line_items_ids}
        return order_items_details_dict

    def get_order_info_by_order_id(self, order_id):
        sql = f"SELECT * FROM {self.db_name}.wp_posts WHERE ID={order_id};"
        return self.db_obj.execute_query(sql)

    ''' Archive methods '''
    # def get_order_items_details(self, order_item_id):
    #     sql = f"SELECT * FROM local.wp_woocommerce_order_itemmeta WHERE order_item_id = {order_item_id};"
    #     rs_sql = self.db_obj.execute_query(sql)
    #     line_details = {k['meta_key']: k['meta_value'] for k in rs_sql}
    #     return line_details




