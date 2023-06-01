from woocommercetest.src.dao.orders_dao import OrdersDAO
from woocommercetest.src.utilities.WooAPIUtility import WooAPIUtility
import json
import os

from woocommercetest.src.utilities.requestsUtility import RequestUtility


class Orders(object):
    def __init__(self):
        self.woo_obj = WooAPIUtility()
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))

    def create_order(self, additional_args=None, expected_status_code=201):
        """
        Create an order based on default order payload in data/create_order_template.json and additional args if given
        Args:
            expected_status_code: int
            additional_args: dict() - additional args to be added to the default template or replace existing ones

        Returns: response - dict

        """
        # using the os.path.join method because in windows data/file-name is different from linux data\file-name
        payload_template_file = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_template.json')
        with open(payload_template_file, 'r') as f:
            payload_data = json.load(f)
        if additional_args:
            assert isinstance(additional_args, dict), f"'Create Order' function parameter 'addition_args' must be a dictionary, but got {type(additional_args)}"
            payload_data.update(additional_args)
        return self.woo_obj.post('orders', 'Create Order', payload_data, expected_status_code)

    def call_update_order(self, order_id, payload, expected_status_code=200):
        return self.woo_obj.put(f'orders/{order_id}', 'Update Order', order_id, payload, expected_status_code=expected_status_code)

    def call_retrieve_order(self, order_id, expected_status_code=200):
        return self.woo_obj.get(f'orders/{order_id}', 'Retrieve Order', expected_status_code=expected_status_code)

    @staticmethod
    def verify_order_response(order_res, exp_cust_id, order_line_items):
        """
        This method verifies the Create Order call response
        Args:
            order_res: response json
            exp_cust_id: int
            order_line_items: list of products dicts

        Returns: None

        """
        # verifying order response is not empty
        assert order_res, "ERROR: Create Order call response is empty"
        # verifying order response customer id matched the given customer id
        assert order_res['customer_id'] == exp_cust_id, f"ERROR: 'Create Order' with given customer_id returned incorrect customer id. Expected customer id: {exp_cust_id} but got" \
        f"{order_res['customer_id']}"
        # verifying number of products in the order response match the number of products given
        assert len(order_res['line_items']) == len(order_line_items), f"ERROR: Expected only {len(order_line_items)} items in the order but found " \
        f"{len(order_res['line_items'])} items"
        # verifying order products id and quantity
        exp_products_dict = {str(p['product_id']): p['quantity'] for p in order_line_items}  # key: product_id, value: product quantity
        for p in order_res['line_items']:
            assert str(p['product_id']) in exp_products_dict, f"ERROR: 'Create order' response includes product id: {str(p['product_id'])} which was not added by the customer." \
            f"Customer id: {exp_cust_id}\nProducts added by customer: {exp_products_dict}"
            assert p['quantity'] == exp_products_dict[str(p['product_id'])], f"ERROR: Unexpected product quantity in 'Create order' response. Product id: {str(p['product_id'])}, " \
                                                                             f"Expected quantity: {exp_products_dict[str(p['product_id'])]} but got {p['quantity']}"

    @staticmethod
    def verify_order_in_db(order_id, order_line_items):
        """
        This method verifies the order and its products are recorded correctly in the DB
        Args:
            order_id: int - order id from order response
            order_line_items: list of api order line items (products) dictionaries

        Returns: None

        """
        orders_dao = OrdersDAO()
        db_lines_info = orders_dao.get_order_lines_by_order_id(order_id)  # list of line items (products)
        # verify list is not empty
        assert db_lines_info, f"ERROR: Create Order, line items not found in db. Order id: {order_id}"
        # verifying number of lines/product found in DB matched the num of lines/products in the response
        db_line_items = list(filter(lambda x: x['order_item_type'] == 'line_item', db_lines_info))
        db_line_items_ids = list(map(lambda x: x['order_item_id'], db_line_items))
        assert len(db_line_items) == len(order_line_items), f"ERROR: Expected {len(order_line_items)} line items but got {len(db_line_items)}. Order ID: {order_id}"
        # verifying line items product_id and quantity in db match the ones in the order response
        db_items_det_dict = orders_dao.get_order_items_details(db_line_items_ids)
        api_items_dict = {k['id']: {"product_id": k['product_id'], "quantity": k['quantity']} for k in order_line_items}
        for line_item_id in api_items_dict.keys():
            assert line_item_id in db_items_det_dict, f"ERROR: order response line itemd id {line_item_id} not found in db. Order id: {order_id}"
            assert str(api_items_dict[line_item_id]['product_id']) == str(db_items_det_dict[line_item_id]['_product_id']), f"ERROR: order line item id {line_item_id} " \
            f"product id in DB doesn't match product id in response. Order response product id: {api_items_dict[line_item_id]['product_id']}, \n" \
            f"DB product id: {db_items_det_dict[line_item_id]['_product_id']}"
            assert str(api_items_dict[line_item_id]['quantity']) == str(db_items_det_dict[line_item_id]['_qty']), f"ERROR: order line item id {line_item_id} " \
            f"product id in DB doesn't match product id in response. Order response product id: {api_items_dict[line_item_id]['quantity']}, \n" \
            f"DB product id: {db_items_det_dict[line_item_id]['_qty']}"












if __name__ == '__main__':
    ord_obj = Orders()
    ord_obj.create_order()