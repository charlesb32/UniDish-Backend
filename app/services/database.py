import mysql.connector

# db_config = {
#     "host": "127.0.0.1",
#     "user": "root",
#     "password": "Capsfan26!",
#     "database": "unidishdb"
# }

db_config = {
    "host": "192.168.1.25",  # replace with the server's IP address
    "user": "charlesb32",
    "password": "Capsfan26!",
    "database": "unidishdb",
    "port": 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)