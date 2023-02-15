import psycopg2
import os

PASSWORD_PG = os.getenv('POSTGRES_PASSWORD') if os.getenv('POSTGRES_PASSWORD') else '0110'

class Query:
    def __init__(self):
        self.conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password=PASSWORD_PG)

    def execute(self, statement):
        cur = self.conn.cursor()
        try:
            cur.execute(statement)
            return cur.fetchall(), 200
        except Exception as e:
            return str(e), 400

    def close(self):
        self.conn.close()

    def get_schema(self, table_name):
        statement = '''select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{}';'''.format(table_name)
        resp, rc = self.execute(statement)
        if rc == 200:
            return [item for inner_list in resp for item in inner_list]
        else:
            return None