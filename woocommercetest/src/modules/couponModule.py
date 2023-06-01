from woocommercetest.src.utilities.WooAPIUtility import WooAPIUtility
import logging as logger


class Coupons(object):
    def __init__(self):
        self.woo_obj = WooAPIUtility()

    def call_list_all_coupons(self, params=None, expected_status_code=200):
        """
        This method gets and returns all the coupons in the system
        Returns: response obj - list of coupons dicts
        """
        logger.debug("Calling 'List all Coupons' request")
        return self.woo_obj.get('coupons', 'List all coupons', params=params, expected_status_code=expected_status_code)

    def call_create_coupons(self, payload, expected_status_code=201):
        """
        This creates a coupon based on input details
        Args:
            expected_status_code: int
            payload: dict - mandatory fields + values for creating a new coupon
        Returns: response object
        """
        if not payload:
            raise Exception("Got an empty payload for creating a coupon")
        logger.debug("Calling 'Create Coupon' request")
        return self.woo_obj.post('coupons', 'Create coupon', payload=payload, expected_status_code=expected_status_code)

    def call_retrieve_coupon(self, coupon_id, expected_status_code=200):
        """
        This method retrieves a coupon given a coupon id
        Args:
            expected_status_code: int
            coupon_id: int
        Returns: response obj - retrieved coupon details
        """
        logger.debug(f"Calling 'Retrieve a coupon' request with id: {coupon_id}")
        return self.woo_obj.get(f"coupons/{coupon_id}", 'Retrieve coupon', expected_status_code=expected_status_code)

    def call_delete_coupon(self, coupon_id, force=False):
        logger.debug(f"Calling 'Delete a coupon' request for coupon id: {coupon_id}")
        return self.woo_obj.delete(f"coupons/{coupon_id}", 'DELETE coupon', force=force)

    def get_generic_coupon_with_percentage(self, discount_amt):
        discount_amt = str("{:.2f}".format(float(discount_amt)))
        all_coupons = self.call_list_all_coupons(params={"per_page": 100})
        logger.debug(f"looking for a coupon with 'percent' discount type and {discount_amt}% discount")
        for coupon in all_coupons:
            if coupon['discount_type'] == 'percent' and coupon['amount'] == discount_amt:
                coupon = coupon
                logger.debug(f"Found the required coupon: {coupon['code']}")
                break
        else:  # no matching coupon was found --> creating a new matching coupon
            logger.debug(f"Did not find the required coupon. Creating a new coupon with {discount_amt} % off")
            data = {
                "code": self.get_coupon_code(discount_amt),
                "discount_type": "percent",
                "amount": discount_amt,
                "individual_use": False,
                "exclude_sale_items": False
            }
            coupon_rs = self.call_create_coupons(data)
            coupon = self.call_retrieve_coupon(coupon_rs['id'])
        return coupon

    @staticmethod
    def get_coupon_code(discount_per, name=None):
        discount = discount_per.strip('0')
        discount = discount[:-1] if discount[-1] == '.' else discount
        name = name if name else '%_off'
        return discount + name




