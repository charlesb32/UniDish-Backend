from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from ..services.database import get_db_connection
from flask_bcrypt import Bcrypt
import jwt
from flask import current_app

auth_blueprint = Blueprint('auth', __name__)
bcrypt = None  # Placeholder for the bcrypt instance

def init_auth_blueprint(bcrypt_instance):
    global bcrypt
    bcrypt = bcrypt_instance

@auth_blueprint.route('/addUser', methods=['POST'])
def add_user():
    user_data = request.json['userData']
    db = get_db_connection()
    cursor = db.cursor()
    if 'confirmPassword' in user_data:
        if user_data['password'] != user_data['confirmPassword']:
            return jsonify({'message' : 'Passwords do not match'}) , 400
    # db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE email=%s", (user_data['email'],))
        user_exists_by_email = cursor.fetchone()[0]  # fetchone returns a tuple, so we take the first element
        if user_exists_by_email:
            # User with this email already exists
            return jsonify({'message': 'User with this email already exists!'}), 400
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
        cursor.execute(insert_query, (user_data['username'], user_data['email'], hashed_password, user_data['type'], '', user_data['firstname'], user_data['lastname']))
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

@auth_blueprint.route('/login', methods=['POST'])
def login():
    user_logging_in = request.json['loginPayload']
    email = user_logging_in['email']
    password = user_logging_in['password']
    hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # print('HASH', hash)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    db_user = cursor.fetchone()
    # print('LOGIN DB USER: ', db_user)
    if not db_user:
        return jsonify({'message': 'No account with this email'}), 401
    # print(email, password)

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

@auth_blueprint.route('/getUserByToken', methods=['GET'])
def get_user_by_token():
    auth_header = request.headers.get('Authorization', None)
    # print('Authheader: ', auth_header)
    if not auth_header:
        return jsonify(message="Missing Authorization Header"), 401

    try:
        # The header format is "Bearer TOKEN", so split by space and get the token
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return jsonify(isLoggedIn=True, user=decoded_token), 200
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token has expired"), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 401
    except Exception as e:
        return jsonify(message=str(e)), 500

@auth_blueprint.route('/updateUserInfo', methods=['PUT'])
def update_user_info():
    db = get_db_connection()
    cursor = db.cursor()
    user_info = request.json['userInfo']
    # print('USERINFO', user_info)
    try:
        cursor.execute("UPDATE USERS SET profile_description = %s WHERE email = %s", (user_info['profile_description'], user_info['email']) )
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@auth_blueprint.route('/updatePassword', methods=['PUT'])
def update_password():
    db = get_db_connection()
    cursor = db.cursor()
    password = request.json['passwordPayload']
    user_id = request.json['userId']
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        db_user = cursor.fetchone()
        # print('DB_USER: ', db_user)
        if bcrypt.check_password_hash(db_user['password'], password['oldPassword']):
            # print('HERE')
            if password['newPassword'] == password['confirmNewPassword']:
                #update password to new pass
                hashed_password = bcrypt.generate_password_hash(password['newPassword']).decode('utf-8')
                cursor.execute("UPDATE USERS SET password = %s WHERE user_id = %s", (hashed_password, user_id) )
                db.commit()
                cursor.close()
                db.close()
                return jsonify({"message": "User Password updated successfully"}), 200
            else:
                cursor.close()
                db.close()
                return jsonify({'message': 'New Password Do not Match'}), 400
                #new passwords no not match
        else:
            # print('HERE2')
            #old password incorrect
            cursor.close()
            db.close()
            return jsonify({'message': 'Old Password is Incorrect'}), 400
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500