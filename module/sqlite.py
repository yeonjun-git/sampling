import sqlite3
import pandas as pd

from fileoperator import BaseOperator

class sqlite:
    
    def __init__(self, data_path):
        self.data_path = data_path
    
    def connect(self):
        return sqlite3.connect(self.data_path)
    
    def execute(self, query):
        conn = self.connect()
        data =  pd.read_sql_query(query, conn)
        conn.close()
        return data
    
if __name__ == '__main__':
       
    data_path = BaseOperator.set_path(
        work_directory='finance',
        target_path='/lotto_data/lotto_data.db'
    )    
        
    db = sqlite(data_path)
    
    query = "select * from tb_lotto_list"
    data = db.execute(query)
    print(data)
    
        