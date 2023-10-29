from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # Import CORS
import mysql.connector
from flask_jwt_extended.exceptions import JWTExtendedException
import jwt

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'
jwt_manager = JWTManager(app)
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

@app.route('/addUser', methods=['POST'])
def add_user():
    user_data = request.json['userData']
    print(user_data)
    if user_data['password'] != user_data['confirmPassword']:
        return jsonify({'message' : 'Passwords do not match'}) , 400
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE email=%s", (user_data['email'],))
        user_exists_by_email = cursor.fetchone()[0]  # fetchone returns a tuple, so we take the first element
        if user_exists_by_email:
            # User with this email already exists
            return jsonify({'message': 'User with this email already exists'}), 400
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE username=%s", (user_data['username'],))
        user_exists_by_username = cursor.fetchone()[0]
        if user_exists_by_username:
            return jsonify({'message': 'User with this username already exists'}), 400
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
         # Given the checks above, if the user does not exist by email or username, proceed to insert
        insert_query = """
        INSERT INTO users (username, email, password, type, profile_description, firstname, lastname)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_data['username'], user_data['email'], hashed_password, 'user', '', user_data['firstname'], user_data['lastname']))
        # Commit the changes to the database
        db.commit()

        # Close the cursor and connection
        cursor.close()
        db.close()
        return jsonify({'message': 'User added successfully'}), 200
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    user_logging_in = request.json['loginPayload']
    email = user_logging_in['email']
    password = user_logging_in['password']

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    db_user = cursor.fetchone()
    
    if not db_user:
        return jsonify({'message': 'No account with this email'}), 401
    print(email, password)

    if bcrypt.check_password_hash(db_user['password'], password):
        payload = {
            'email': db_user['email'],
            'id': db_user['user_id'],
            'firstname': db_user['firstname'],
            'lastname': db_user['lastname'],
            'username': db_user['username'],
            'type': db_user['type'],
            'profile_description': db_user['profile_description']
        }
        token = create_access_token(identity=payload, expires_delta=False)
         # Close the cursor and connection
        cursor.close()
        db.close()
        return jsonify({'message': 'Success', 'token': 'Bearer ' + token}), 200
     # Close the cursor and connection
    cursor.close()
    db.close()
    return jsonify({'message': 'Wrong Password'}), 400

@app.route('/getUserByToken', methods=['GET'])
def get_user_y_token():
    auth_header = request.headers.get('Authorization', None)
    print('Authheader: ', auth_header)
    if not auth_header:
        return jsonify(message="Missing Authorization Header"), 401

    try:
        # The header format is "Bearer TOKEN", so split by space and get the token
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return jsonify(isLoggedIn=True, user=decoded_token), 200
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token has expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 401
    except Exception as e:
        return jsonify(message=str(e)), 500

@app.errorhandler(JWTExtendedException)
def handle_jwt_extended_error(err):
    print("JWT Error:", str(err))
    return jsonify(message="JWT Error: " + str(err)), 422

if __name__ == '__main__':
    app.run(debug=True)