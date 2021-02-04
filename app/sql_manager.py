import sqlite3
from sqlite3 import Error
import os
from pathlib import Path
from datetime import datetime

class sqlManager():
    _sql_create_products_table = """ CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        upc text NOT NULL,
                                        ean text NOT NULL,
                                        name text,
                                        desc text,
                                        lprice real
                                    ); """

    _conn = None
    _curs = None

    def __init__(self, db_name=None):
        if (db_name == None):
            date = datetime.now()
            date = date.strftime("%d%m%Y-%H%M%S")
            self._session_db = os.path.join(str(Path.home()), "productdb_" + date + ".db")
        else:
            self._session_db = os.path.join(str(Path.home()), db_name + ".db")
        self._conn = self.__connect_to_db(self._session_db)
        self._curs = self.__create_table(self._sql_create_products_table)

    def __connect_to_db(self, db_file):
        #if (not os.path.exists(db_file)):
        return sqlite3.connect(db_file)
        #else:
        #    return None

    def __create_table(self, create_table_sql):
        try:
            c = self._conn.cursor()
            c.execute(create_table_sql)
            return c
        except Error as e:
            print(e)
        return None

    def create_product(self, product):
        self._curs.execute("SELECT * FROM products WHERE id=?", (product[0],))
        records = self._curs.fetchall()

        if (len(records) == 0):
            sql = ''' INSERT INTO products (upc,ean,name,desc,lprice)
                  VALUES(?,?,?,?,?) '''
            self._curs.execute(sql, product)
            self._conn.commit()
        return self._curs.lastrowid

    def update_product(self, product):
        # Find product by either upc or ean, whichever is available
        if (product[0].isnumeric()):
            self._curs.execute("SELECT * FROM products WHERE upc=?", (product[0],))
        else:
            self._curs.execute("SELECT * FROM products WHERE ean=?", (product[1],))

        # Id will be first value in returned tuple
        id = self._curs.fetchone()[0]

        sql = ''' UPDATE products
                  SET upc = ?,
                      ean = ?,
                      name = ?,
                      desc = ?,
                      lprice = ?
                  WHERE id = ?'''
        self._curs.execute(sql, product + (id,))
        self._conn.commit()

    def select_all_products(self):
        self._curs.execute("SELECT * FROM products")
        rows = self._curs.fetchall()
        return rows

    def select_product_by_upc(self, upc):
        self._curs.execute("SELECT * FROM products WHERE upc=?", (str(upc),))
        return self._curs.fetchall()

    def select_product_by_ean(self, ean):
        self._curs.execute("SELECT * FROM products WHERE ean=?", (str(ean),))
        return self._curs.fetchall()

    def get_db_path(self):
        return self._session_db