import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='',
        database='student_result_db'
    )
