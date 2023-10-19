from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

db_config = {
    "host": "127.0.0.1",
    "user": "charlesb32",
    "password": "Capsfan26!",
    "database": "unidashdb"
}

# Create a MySQL connection
db = mysql.connector.connect(**db_config)

# Create a cursor to interact with the database
cursor = db.cursor()
# print('hgadsfad')
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Create a MySQL connection and cursor within the route
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Example: Execute a query to fetch data from the database
        cursor.execute("SELECT * FROM dining_halls")
        data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        db.close()

        return jsonify({"status": "Connected to DBMS successfully!", "data": data})
    except Exception as e:
        return jsonify({"status": "Failed to connect to the DBMS", "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)