from flask import Flask
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "127.0.0.1",
    "user": "admin",
    "password": "unidish_admin",
    "database": "admin-unidish"
}

# Create a MySQL connection
db = mysql.connector.connect(**db_config)

# Create a cursor to interact with the database
cursor = db.cursor()

@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Example: Execute a query to fetch data from the database
        cursor.execute("SELECT * FROM RESTAURANT")
        return jsonify("Connected")
    except Exception as e:
        return jsonify("Failed to connect to the DBMS")

if __name__ == '__main__':
    app.run()