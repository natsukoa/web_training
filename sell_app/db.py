from config import config
from psycopg2 import connect
from psycopg2.extras import DictCursor
from logging import getLogger
from singleton import Singleton


logger = getLogger(__name__)


class DB(object, metaclass=Singleton):

    def __init__(self):
        db = config['db']
        host = db['host']
        user = db['user']
        password = db['password']
        db_name = db['db_name']

        self.conn = connect(
            'dbname={} host={} user={} password={}'.format(db_name,
                                                           host,
                                                           user,
                                                           password))

    def __del__(self):
        self.conn.close()

    def select_execute(self, sql, values=()):
        results = []
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(sql, values)

                print(cur.query)
                rows = cur.fetchall()
                results = [dict(row) for row in rows]

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

        return results
    
    
    def execute(self, sql):
        try:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(sql)

                print(cur.query)

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

        return