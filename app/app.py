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
@app.route('/getDiningHallsWithRestaurants', methods=['GET'])
def get_dining_halls_with_restaurants():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM DINING_HALLS")
        dining_halls = cursor.fetchall()
        # print('DINING HALLS: ', dining_halls)
        result = []
        for dining_hall in dining_halls:
            dh_id, dh_name, dh_address, dh_rating, dh_description = dining_hall
            print('DINING HALL: ', dh_id)
            cursor.execute("SELECT * FROM RESTAURANTS WHERE dining_hall_id=%s", (dh_id,))
            restaurants = cursor.fetchall()
            print('RESTAURANTS: ', restaurants)
            restaurants_list = [{
                'id': r[0],
                'name': r[1],
                'overall_rating': r[2],
                'description' : r[3],
                'menu_name': r[4],
                'menu_description': r[5],
                'dining_hall_id': r[6]
                } for r in restaurants]
            result.append({
                'dining_hall': dining_hall,
                'restaurants': restaurants_list
                })
        cursor.close()
        db.close()
        return jsonify({'dining_halls': result})
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

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
    hash = bcrypt.generate_password_hash(password).decode('utf-8')
    print('HASH', hash)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    db_user = cursor.fetchone()
    print('LOGIN DB USER: ', db_user)
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

@app.route('/getRestaurantById', methods=['GET'])
def get_restaurant_by_id():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        rest_id = request.args.get('restId')
        print(rest_id)
        cursor.execute("SELECT * FROM RESTAURANTS WHERE restaurant_id=%s", (rest_id,))
        restaurant = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify({'restaurant': restaurant})
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500


@app.route('/getMenuItemsForRestaurant', methods=['GET'])
def get_menu_items_for_restaurant():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        rest_id = request.args.get('restId')
        print(rest_id)
        cursor.execute("SELECT * FROM menu_items WHERE restaurant_id=%s", (rest_id,))
        menu_items = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify({'menu_items': menu_items})
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@app.route('/updateUserInfo', methods=['PUT'])
def update_user_info():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    user_info = request.json['userInfo']
    print('USERINFO', user_info)
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

@app.route('/updatePassword', methods=['PUT'])
def update_password():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    password = request.json['passwordPayload']
    user_id = request.json['userId']
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        db_user = cursor.fetchone()
        print('DB_USER: ', db_user)
        if bcrypt.check_password_hash(db_user['password'], password['oldPassword']):
            print('HERE')
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
            print('HERE2')
            #old password incorrect
            cursor.close()
            db.close()
            return jsonify({'message': 'Old Password is Incorrect'}), 400
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500
    print('PASSWORD PAYLOAFD: ', password_info, user_id)

@app.route('/addDiningHall', methods=['POST'])
def add_dining_hall():
    dining_hall_data = request.json['diningHallData']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(dining_hall_data)
    try:
        cursor.execute('INSERT INTO DINING_HALLS (dining_hall_name, description, dining_hall_address) VALUES (%s, %s, %s)', (dining_hall_data['name'], dining_hall_data['description'], dining_hall_data['address']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Dining Hall Added successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@app.route('/addRestaurant', methods=['POST'])
def add_restaurant():
    rest_data = request.json['restData']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(rest_data)
    try:
        cursor.execute('INSERT INTO RESTAURANTS (name, description, dining_hall_id) VALUES (%s, %s, %s)', (rest_data['name'], rest_data['description'], rest_data['diningHallId']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Restaurant Added successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@app.route('/deleteRestaurant/<int:rest_id>', methods=['DELETE'])
def delete_restaurant(rest_id):
    print('REST_ID: ', rest_id)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM RESTAURANTS WHERE restaurant_id = %s", (rest_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Restaurant deleted successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/deleteDiningHall/<int:dining_hall_id>', methods=['DELETE'])
def delete_dining_hall(dining_hall_id):
    print('DINING_HALL_ID: ', dining_hall_id)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM DINING_HALLS WHERE dining_hall_id = %s", (dining_hall_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Dining hall deleted successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/editRestaurant', methods=['PUT'])
def edit_restaurant():
    rest = request.json['restData']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(rest)
    try:
        cursor.execute("UPDATE RESTAURANTS SET name = %s, description = %s WHERE restaurant_id=%s", (rest['name'], rest['description'], rest['diningHallId']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Restaurant Updated successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/editDiningHall', methods=['PUT'])
def edit_dining_hall():
    dining_hall = request.json['diningHallData']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(dining_hall)
    try:
        cursor.execute("UPDATE DINING_HALLS SET dining_hall_name = %s, description = %s, dining_hall_address = %s WHERE dining_hall_id=%s", (dining_hall['name'], dining_hall['description'], dining_hall['address'], dining_hall['id']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Dining Hall Updated successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/editMenuItem', methods=['PUT'])
def edit_menu_item():
    menu_item = request.json['menuItem']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(menu_item)
    try:
        cursor.execute("UPDATE MENU_ITEMS SET name = %s, description = %s, calorie_count = %s, price = %s WHERE menu_item_id= %s", (menu_item['name'], menu_item['description'], menu_item['calories'],  menu_item['price'], menu_item['id']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Menu Item Updated successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/addMenuItem' , methods=['POST'])
def add_menu_item():
    menu_item = request.json['menuItem']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print(menu_item)
    try:
        cursor.execute('INSERT INTO MENU_ITEMS (name, description, calorie_count, price, restaurant_id) VALUES (%s, %s, %s, %s, %s)', (menu_item['name'], menu_item['description'], menu_item['calories'], menu_item['price'], menu_item['restaurantId']))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Restaurant Added successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)