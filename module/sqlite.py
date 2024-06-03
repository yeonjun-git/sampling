import sqlite3
import pandas as pd

from fileoperator import BaseOperator

class SqliteSQL:
    
    def __init__(self, data_path):
        self.data_path = data_path
    
    def connect(self, db_file=None):
        if db_file is None:
            conn = sqlite3.connect(self.data_path)
            print(f"Connected to {self.data_path}")
        else:
            conn = sqlite3.connect(db_file)
            print(f"Connected to {db_file}")
            
        self.conn = conn
        return self.conn
    
    def execute(self, query):
        data =  pd.read_sql_query(query, self.conn)
        self.conn.close()
        return data
    
if __name__ == '__main__':
       pass