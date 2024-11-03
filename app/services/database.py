import mysql.connector

# db_config = {
#     "host": "127.0.0.1",
#     "user": "root",
#     "password": "Capsfan26!",
#     "database": "unidishdb"
# }

# db_config = {
#     "host": "192.168.1.25",  # replace with the server's IP address
#     "user": "charlesb32",
#     "password": "Capsfan26!",
#     "database": "unidishdb",
#     "port": 3306
# }

# Updated db_config for Amazon RDS
db_config = {
    "host": "unidish-db.c102cukc07ig.us-east-1.rds.amazonaws.com",  # Your RDS endpoint
    # "user": "charlesb32",             # RDS username
    "user": "admin",             # RDS username
    "password": "Capsfan26!",         # RDS password
    "database": "unidish_db",           # RDS database name
    "port": 3306                       # Default MySQL port
}

def get_db_connection():
    return mysql.connector.connect(**db_config)