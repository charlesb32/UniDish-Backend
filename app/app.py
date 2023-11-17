from flask import Flask, jsonify, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # Import CORS
import mysql.connector
from flask_jwt_extended.exceptions import JWTExtendedException
import jwt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime, timedelta
# import matplotlib 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# matplotlib.use('Agg')
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
            # print('DINING HALL: ', dh_id)
            cursor.execute("SELECT * FROM RESTAURANTS WHERE dining_hall_id=%s", (dh_id,))
            restaurants = cursor.fetchall()
            # print('RESTAURANTS: ', restaurants)
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
    # print(user_data)
    if 'confirmPassword' in user_data:
        if user_data['password'] != user_data['confirmPassword']:
            return jsonify({'message' : 'Passwords do not match'}) , 400
    db = mysql.connector.connect(**db_config)
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

@app.route('/login', methods=['POST'])
def login():
    user_logging_in = request.json['loginPayload']
    email = user_logging_in['email']
    password = user_logging_in['password']
    hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # print('HASH', hash)
    db = mysql.connector.connect(**db_config)
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

@app.route('/getUserByToken', methods=['GET'])
def get_user_y_token():
    auth_header = request.headers.get('Authorization', None)
    # print('Authheader: ', auth_header)
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
        # print(rest_id)
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
        # print(rest_id)
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
    # print('PASSWORD PAYLOAFD: ', password_info, user_id)

@app.route('/addDiningHall', methods=['POST'])
def add_dining_hall():
    dining_hall_data = request.json['diningHallData']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    # print(dining_hall_data)
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
    # print(rest_data)
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
    # print('REST_ID: ', rest_id)
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
    # print('DINING_HALL_ID: ', dining_hall_id)
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
    # print(rest)
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
    # print(dining_hall)
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
    # print(menu_item)
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

@app.route('/deleteMenuItem/<int:menu_item_id>', methods=['DELETE'])
def delete_menu_item(menu_item_id):
    # print('MENU_ITEM_ID: ', menu_item_id)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM MENU_ITEMS WHERE menu_item_id = %s", (menu_item_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Menu item deleted successfully"}), 200
    except Exception as e:
        cursor.close()
        db.close()  
        return jsonify({'message': str(e)}), 500

@app.route('/addMenuItem' , methods=['POST'])
def add_menu_item():
    menu_item = request.json['menuItem']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    # print(menu_item)
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

def get_review_likes(post_id, post_type):
    # print('POST ID: ', post_id)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        query = ''
        if post_type == 'review':
            query = """
            SELECT COUNT(*) AS likes_count
            FROM review_likes
            WHERE rreview_id = %s
            """
        elif post_type == 'comment':
            query = """
            SELECT COUNT(*) AS likes_count
            FROM comment_likes
            WHERE ccomment_id = %s
            """
        cursor.execute(query, (post_id,))
        result = cursor.fetchone()  # Fetch the result
        return result['likes_count'] if result else 0
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_review_dislikes(post_id, post_type):
    # print('POST ID: ', post_id)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        query = ''
        if post_type == 'review':
            query = """
            SELECT COUNT(*) AS dislikes_count
            FROM review_dislikes
            WHERE rreview_id = %s
            """
        elif post_type == 'comment':
            query = """
            SELECT COUNT(*) AS dislikes_count
            FROM comment_dislikes
            WHERE ccomment_id = %s
            """
        cursor.execute(query, (post_id,))
        result = cursor.fetchone()  # Fetch the result
        return result['dislikes_count'] if result else 0
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_user(user_id):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        query = """
        SELECT * 
        FROM users
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  # Fetch the result
        # print('USER: ', result)
        return result
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_highlight(user_id, post_id, post_type):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    # print('USER AND POST IDS', user_id, post_id)
    try:
        like_query = ''
        dislike_query = ''
        if post_type == 'review':
            like_query = """
            SELECT * FROM review_likes
            WHERE uuser_id = %s AND rreview_id = %s
            """
            cursor.execute(like_query, (user_id, post_id))
            like_result = cursor.fetchone()  # Fetch the result
            # print('LIKE_RESULT: ',like_result)
            if like_result:
                return 'like'
            dislike_query = """
            SELECT * FROM review_dislikes
            WHERE uuser_id = %s AND rreview_id = %s
            """
            cursor.execute(dislike_query, (user_id, post_id))
            dislike_result = cursor.fetchone()  # Fetch the result
            if dislike_result:
                return 'dislike'
        elif post_type == 'comment':
            like_query = """
            SELECT * FROM comment_likes
            WHERE uuser_id = %s AND ccomment_id = %s
            """
            cursor.execute(like_query, (user_id, post_id))
            like_result = cursor.fetchone()  # Fetch the result
            # print('LIKE_RESULT: ',like_result)
            if like_result:
                return 'like'
            dislike_query = """
            SELECT * FROM comment_dislikes
            WHERE uuser_id = %s AND ccomment_id = %s
            """
            cursor.execute(dislike_query, (user_id, post_id))
            dislike_result = cursor.fetchone()  # Fetch the result
            if dislike_result:
                return 'dislike'
        return ''
    except Exception as e:
        # print(f"Error getting highlight info: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()
@app.route('/getReviews', methods=['GET'])
def get_reviews_and_review_info():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        rest_id = request.args.get('restId')
        # print('REST_ID: ', rest_id)
        curr_user_id = request.args.get('currUserId')
        # print('CURRUSERID: ', curr_user_id)
        query = """
        SELECT * FROM reviews 
        WHERE restaurant_id = %s 
        ORDER BY date DESC
        """
        cursor.execute(query, (rest_id,))  # Note the comma for a single parameter
        reviews = cursor.fetchall()
        for review in reviews:
            review['likes'] = get_review_likes(review['review_id'], 'review')
            review['dislikes'] = get_review_dislikes(review['review_id'], 'review')
            review['user'] = get_user(review['user_id'])
            review['highlight'] = get_highlight(curr_user_id, review['review_id'], 'review')
        # print('REVIEWS: ', reviews)
        cursor.close()
        db.close()
        return jsonify(reviews)
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@app.route('/like', methods=['POST'])
def add_like():
    like_info = request.json['likeInfo']
    # print(like_info)
    user_id = like_info['userId']
    post_id = like_info['postId']
    like_type = like_info['likeType']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        if like_type == 'review':
        # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM review_likes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            like_result = cursor.fetchone()

            if like_result['like_count'] > 0:
                #if already liked remove the like
                cursor.execute("""
                    DELETE FROM review_likes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review unliked'}), 200
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM review_dislikes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['dislike_count'] > 0:
                # User has disliked the review, remove the dislike
                cursor.execute("""
                    DELETE FROM review_dislikes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
            # Now add the like (after removing dislike if it was there)
            cursor.execute("""
                INSERT INTO review_likes (uuser_id, rreview_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        elif like_type == 'comment':
        # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM comment_likes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            like_result = cursor.fetchone()

            if like_result['like_count'] > 0:
                #if already liked remove the like
                cursor.execute("""
                    DELETE FROM comment_likes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review unliked'}), 200
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM comment_dislikes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['dislike_count'] > 0:
                # User has disliked the review, remove the dislike
                cursor.execute("""
                    DELETE FROM comment_dislikes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
            # Now add the like (after removing dislike if it was there)
            cursor.execute("""
                INSERT INTO comment_likes (uuser_id, ccomment_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        return jsonify({'message': 'Like added successfully'}), 200

    except Exception as e:
        db.rollback()
        # print(f"Error in add_like: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/dislike', methods=['POST'])
def add_dislike():
    dislike_info = request.json['dislikeInfo']
    # print(dislike_info)
    user_id = dislike_info['userId']
    post_id = dislike_info['postId']
    dislike_type = dislike_info['dislikeType']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        if dislike_type == 'review':
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM review_dislikes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            dislike_result = cursor.fetchone()

            if dislike_result['dislike_count'] > 0:
                # User has already disliked the review, remove dislike
                cursor.execute("""
                    DELETE FROM review_dislikes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review undisliked'}), 200
            # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM review_likes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['like_count'] > 0:
                # User has liked the review, remove the like
                cursor.execute("""
                    DELETE FROM review_likes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()

            # Now add the dislike (after removing like if it was there)
            cursor.execute("""
                INSERT INTO review_dislikes (uuser_id, rreview_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        elif dislike_type == 'comment':
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM comment_dislikes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            dislike_result = cursor.fetchone()

            if dislike_result['dislike_count'] > 0:
                # User has already disliked the review, remove dislike
                cursor.execute("""
                    DELETE FROM comment_dislikes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review undisliked'}), 200
            # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM comment_likes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['like_count'] > 0:
                # User has liked the review, remove the like
                cursor.execute("""
                    DELETE FROM comment_likes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()

            # Now add the dislike (after removing like if it was there)
            cursor.execute("""
                INSERT INTO comment_dislikes (uuser_id, ccomment_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        return jsonify({'message': 'Dislike added successfully'}), 200

    except Exception as e:
        db.rollback()
        # print(f"Error in add_like: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/getOverallRestaurantRating', methods=['GET'])
def get_overall_restaurant_rating():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    rest_id = request.args.get('restId')
    # print('REST_ID:!!!!!!!!! ', rest_id)
    try:
        query = "SELECT AVG(rating) as average_rating FROM reviews WHERE restaurant_id = %s"
        cursor.execute(query, (rest_id,))
        result = cursor.fetchone()
        average_rating = result['average_rating'] if result['average_rating'] is not None else 0
        return jsonify({'averageRating': average_rating}), 200
        
    except Exception as e:
        db.rollback()
        # print(f"Error in get_overall_restaurant_rating: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()


@app.route('/createReview', methods=['POST'])
def create_review():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    review_info = request.json['reviewInfo']
    rating = review_info['rating']
    description = review_info['description']
    user_id = review_info['userId']
    rest_id = review_info['restaurantId']
    date = review_info['date']
    try:
        cursor.execute("""
        INSERT INTO reviews (date, rating, description, restaurant_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (date, rating, description, rest_id, user_id))
        db.commit()
        return jsonify({'message': 'Review added successfully'}), 200
    except Exception as e:
        # print(f"Error in create_review: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/createComment', methods=['POST'])
def create_comment():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    comment_info = request.json['commentInfo']
    description = comment_info['description']
    user_id = comment_info['userId']
    date = comment_info['date']
    review_id = comment_info['reviewId']
    try:
        cursor.execute("""
        INSERT INTO comments (description, user_id, review_id, date)
        VALUES (%s, %s, %s, %s)
        """, (description, user_id, review_id, date))
        db.commit()
        return jsonify({'message': 'Comment added successfully'}), 200
    except Exception as e:
        # print(f"Error in create_comment: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/getComments', methods=['GET'])
def get_review_comments():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    review_id = request.args.get('reviewId')
    curr_user_id = request.args.get('currUserId')
    # print('REST_ID:!!!!!!!!! ', rest_id)
    try:
        query = "SELECT * FROM comments WHERE review_id = %s ORDER BY date DESC"
        cursor.execute(query, (review_id,))
        comments = cursor.fetchall()
        for comment in comments:    
            comment['likes'] = get_review_likes(comment['comment_id'], 'comment')
            comment['dislikes'] = get_review_dislikes(comment['comment_id'], 'comment')
            comment['user'] = get_user(comment['user_id'])
            comment['highlight'] =  get_highlight(curr_user_id, comment['comment_id'], 'comment')
            # print('COMMENTS: ', comments)
        return jsonify({'comment': comments}), 200
        
    except Exception as e:
        # print(f"Error in get_review_comments: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/getWeeklyReviewReport', methods=['GET'])
def get_weekly_review_report():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # Calculate the date two months ago from today
    two_months_ago = datetime.now() - timedelta(days=60)

    # SQL query to count reviews per week for the last two months
    query = """
    SELECT YEARWEEK(date) as review_week, COUNT(*) as review_count
    FROM reviews
    WHERE date >= %s
    GROUP BY YEARWEEK(date)
    ORDER BY YEARWEEK(date)
    """

    # Execute the query
    cursor.execute(query, (two_months_ago,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

     # Prepare data for plotting
    date_ranges = []
    counts = []
    for result in results:
        year_week = str(result['review_week'])
        year = int(year_week[:4])
        week = int(year_week[4:]) - 1
        week_start = datetime(year, 1, 1) + timedelta(weeks=week)
        if week_start.weekday() > 0:
            week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=6)
        date_range = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
        date_ranges.append(date_range)
        counts.append(result['review_count'])

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(date_ranges, counts, marker='o')
    plt.title('Number of Reviews Written per Week')
    plt.xlabel('Date Range')
    plt.ylabel('Number of Reviews')

    # Adjust x-axis labels: smaller font and horizontal alignment
    plt.xticks(rotation=0, fontsize=8)  # Change rotation to 0 and adjust font size as needed
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object to send as a response
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Send the image in the response
    return send_file(img, mimetype='image/png')

@app.route('/getWeeklyCommentReport', methods=['GET'])
def get_weekly_comment_report():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # Calculate the date two months ago from today
    two_months_ago = datetime.now() - timedelta(days=60)

    # SQL query to count reviews per week for the last two months
    query = """
    SELECT YEARWEEK(date) as comment_week, COUNT(*) as comment_count
    FROM comments
    WHERE date >= %s
    GROUP BY YEARWEEK(date)
    ORDER BY YEARWEEK(date)
    """

    # Execute the query
    cursor.execute(query, (two_months_ago,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

     # Prepare data for plotting
    date_ranges = []
    counts = []
    for result in results:
        year_week = str(result['comment_week'])
        year = int(year_week[:4])
        week = int(year_week[4:]) - 1
        week_start = datetime(year, 1, 1) + timedelta(weeks=week)
        if week_start.weekday() > 0:
            week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=6)
        date_range = f"{week_start.strftime('%Y/%m/%d')} - {week_end.strftime('%Y/%m/%d')}"
        date_ranges.append(date_range)
        counts.append(result['comment_count'])

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(date_ranges, counts, marker='o')
    plt.title('Number of Comments Written per Week')
    plt.xlabel('Date Range')
    plt.ylabel('Number of Comments')

    # Adjust x-axis labels: smaller font and horizontal alignment
    plt.xticks(rotation=0, fontsize=8)  # Change rotation to 0 and adjust font size as needed
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a BytesIO object to send as a response
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Send the image in the response
    return send_file(img, mimetype='image/png')

@app.route('/getTop3MostActiveUsersReport', methods=['GET'])
def get_top_three_most_active_users_report():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # SQL query to fetch the top 3 users based on total comments and reviews
    query = """
    SELECT u.username, SUM(total_activities) as total_activities
    FROM (
        SELECT user_id, COUNT(*) as total_activities FROM reviews GROUP BY user_id
        UNION ALL
        SELECT user_id, COUNT(*) FROM comments GROUP BY user_id
    ) as combined
    INNER JOIN users u ON combined.user_id = u.user_id
    GROUP BY combined.user_id
    ORDER BY total_activities DESC
    LIMIT 3
    """


    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    db.close()

    # Process the results for plotting
    usernames = [result['username'] for result in results]
    activities = [result['total_activities'] for result in results]

    # Generate the bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(usernames, activities, color='blue')
    plt.title('Top 3 Most Active Users')
    plt.xlabel('Username')
    plt.ylabel('Total Number of Comments and Reviews')

    plt.xticks(usernames)  # Set user IDs as x-axis labels
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Send the image in the response
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, threaded=False) #need this to work for matplotlib to not break