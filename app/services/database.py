import mysql.connector

db_config = {
    "host": "127.0.0.1",
    "user": "charlesb32",
    "password": "Capsfan26!",
    "database": "unidashdb"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)