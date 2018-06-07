# -*- coding: UTF-8 -*-
import MySQLdb


class MyDB(object):
    def __init__(self, db_address="localhost", usr="root", pwd="Abc12345"):
        self.db_address = db_address
        self.usr = usr
        self.pwd = pwd

    def get_connection(self, schemas_name):
        return MySQLdb.connect(self.db_address, self.usr, self.pwd, schemas_name, charset='utf8')

    def get_cursor(self, db_connection):
        return db_connection.cursor()

    def colse(self, db_connection):
        return db_connection.close()
