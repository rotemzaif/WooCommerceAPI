import pymysql
import os
import logging as logger
from woocommercetest.src.utilities.credentialsUtility import CredentialsUtility
from woocommercetest.src.configs.hosts_config import DB_HOSTS


class DBUtility(object):

    def __init__(self):
        self.creds = CredentialsUtility().get_db_credentials()
        self.machine = os.environ.get('MACHINE')
        assert self.machine, f"Environment variable 'MACHINE' mus be set"
        self.wp_host = os.environ.get('WP_HOST')
        assert self.machine, f"Environment variable 'WP_HOST' mus be set"
        if self.machine == 'docker' and self.wp_host == 'local':
            raise Exception("Cannot run test in docker if WP_HOST=local")
        self.env = os.environ.get('ENV', 'test')
        self.host = DB_HOSTS[self.machine][self.env]['host']
        self.port = DB_HOSTS[self.machine][self.env]['port']
        self.database = DB_HOSTS[self.machine][self.env]['database']
        self.table_prefix = DB_HOSTS[self.machine][self.env]['table_prefix']

    def execute_query(self, query):
        conn = self.create_connection()
        try:
            logger.debug(f"Executing query: {query}")
            cursor = conn.cursor(pymysql.cursors.DictCursor)  # will return each record as a dict
            cursor.execute(query)
            rs_list_dict = cursor.fetchall()
            cursor.close()
        except Exception as e:
            raise Exception(f"Failed to execute query: {query}\nError: {e}")
        finally:
            conn.close()
        return rs_list_dict

    def create_connection(self):
        logger.debug(f"Connecting to DB with the following parameters: host: {self.host}, user: {self.creds['db_user']}, password: {self.creds['db_password']}, "
                     f"port: {self.port}")
        connection = pymysql.connect(host=self.host, user=self.creds['db_user'], password=self.creds['db_password'], port=self.port)
        if not connection:
            raise Exception("Failed to connect to DB")
        return connection

