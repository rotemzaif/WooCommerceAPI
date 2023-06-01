import logging as logger
import random
import string


def generate_random_email_and_password(domain=None, email_prefix=None):
    logger.debug("Generating random email and password")
    if not domain:
        domain = "woocommerce.com"
    if not email_prefix:
        email_prefix = "testuser"
    random_email_string_length = 10
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_length))
    email = email_prefix + '_' + random_string + '@' + domain
    password_length = 20
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))
    random_info = {'email': email, 'password': password_string}
    logger.debug(f'Randomly generated email and password: {random_info}')
    return random_info


def generate_random_string(length=10, prefix=None, suffix=None):
    logger.debug("Generating random string")
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    if prefix:
        random_string = prefix + " " + random_string
    if suffix:
        random_string = random_string + " " + suffix
    logger.debug(f'Randomly generated string: {random_string}')
    return random_string


def generate_random_coupon_code(discount_pct, prefix=None, length=10, ):
    logger.debug("Generating random coupon code")
    discount_pct = discount_pct.strip('0')
    discount_pct = discount_pct[:-1] if discount_pct[-1] == '.' else discount_pct
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    if prefix:
        coupon_code = prefix + "_" + random_string + "_" + discount_pct + "%off"
    else:
        coupon_code = random_string + "_" + discount_pct + "%off"
    logger.debug(f'Randomly generated coupon code: {coupon_code}')
    return coupon_code




