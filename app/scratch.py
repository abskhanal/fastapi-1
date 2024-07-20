import pyodbc
import time

SERVER = 'BZCFR93LT'
DATABASE = 'Customer'

DRIVER = '{ODBC Driver 17 for SQL Server}'

connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'


while True:
    try:
        conn = pyodbc.connect(connectionString)
        print("Connection Successful!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)
        

query = """
select * from Customer
"""
def get_dict(query):
    cursor = conn.cursor().execute(query)
    keys = [column[0] for column in cursor.description]
    values = cursor.fetchall()
    data = []
    for value in values:
        data_item = dict(zip(keys, value))
        data.append(data_item)
    return data

