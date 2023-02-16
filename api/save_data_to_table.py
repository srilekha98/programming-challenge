import os
import re
import psycopg2
import csv

CREATE_TABLE = "CREATE"
INSERT_ROW = "INSERT"
PASSWORD_PG = "POSTGRES_PASSWORD"
STMTS = {
      CREATE_TABLE: '''CREATE TABLE {} ( {} );''',
      INSERT_ROW: '''INSERT INTO {} ( {} ) VALUES ( {} );''',
     }

class SaveData:

    def __init__(self):
        self.tables = self.get_table_names()

    def execute_sql_statement(self, statement):
        print(os.getenv(PASSWORD_PG))
        conn = psycopg2.connect(
                  host="localhost",
                  database="postgres",
                  user="postgres",
                  password=os.getenv(PASSWORD_PG))
        cursor =  conn.cursor()
        try:
            cursor.execute(statement)
            conn.commit()
            return "Success", 200
        except psycopg2.Error as e:
            return str(e), 400
        finally:
            conn.close()

    def read_table_columns(self, file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            cols = []
            for row in csv_reader:
                cols.append(row)
                break
            return cols[0][1:]

    def read_table_rows(self, file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            next(csv_reader)
            list_of_rows = []
            for row in csv_reader:
                list_of_rows.append(row)
            return list_of_rows

    def get_insert_statements(self, table_name):
        rows = self.read_table_rows("data/{}.csv".format(table_name))
        items_to_insert = []
        columns = "Id,"+",".join(self.get_column_names(table_name))
        for item in rows:
            items_to_insert.append(["'{}',".format(each_item) for each_item in item])
        return [ STMTS[INSERT_ROW].format(table_name, columns,"".join(items).rstrip(',')) for items in items_to_insert ]

    def write_rows(self):
        for table in self.tables:
            statements_to_execute = self.get_insert_statements(table)
            for statement in statements_to_execute:
                try:
                    self.execute_sql_statement(statement)
                except Exception as e:
                    print(e)
                    return False
        return True

    def get_column_names(self, table_name):
        return [ re.sub('[^a-zA-Z0-9 _\-\n\.]', '', column_name) for column_name in self.read_table_columns("data/{}.csv".format(table_name))]

    def get_table_names(self):
        return [item.split(".")[0] for item in os.listdir("data")]

    def columns_stmt(self, table_name):
        statement = "Id varchar(256) NOT NULL,"+"".join("{} varchar(256),".format(column) for column in self.get_column_names(table_name))
        return statement.rstrip(',')

    def create_tables(self):
        for table in self.tables:
            statement = STMTS[CREATE_TABLE].format(table,self.columns_stmt(table))
            try:
                self.execute_sql_statement(statement)
            except Exception as e:
                print(e)
                return False
        return True


obj = SaveData()
if obj.create_tables():
    print(obj.write_rows())