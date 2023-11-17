from flask import Blueprint, jsonify, request
from ..services.database import get_db_connection

dining_blueprint = Blueprint('dining', __name__)

@dining_blueprint.route('/getDiningHallsWithRestaurants', methods=['GET'])
def get_dining_halls_with_restaurants():
    db = get_db_connection()
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

@dining_blueprint.route('/getRestaurantById', methods=['GET'])
def get_restaurant_by_id():
    db = get_db_connection()
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
    

@dining_blueprint.route('/getMenuItemsForRestaurant', methods=['GET'])
def get_menu_items_for_restaurant():
    db = get_db_connection()
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

@dining_blueprint.route('/addDiningHall', methods=['POST'])
def add_dining_hall():
    dining_hall_data = request.json['diningHallData']
    db = get_db_connection()
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

@dining_blueprint.route('/addRestaurant', methods=['POST'])
def add_restaurant():
    rest_data = request.json['restData']
    db = get_db_connection()
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

@dining_blueprint.route('/deleteRestaurant/<int:rest_id>', methods=['DELETE'])
def delete_restaurant(rest_id):
    db = get_db_connection()
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

@dining_blueprint.route('/deleteDiningHall/<int:dining_hall_id>', methods=['DELETE'])
def delete_dining_hall(dining_hall_id):
    db = get_db_connection()
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

@dining_blueprint.route('/editRestaurant', methods=['PUT'])
def edit_restaurant():
    rest = request.json['restData']
    db = get_db_connection()
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

@dining_blueprint.route('/editDiningHall', methods=['PUT'])
def edit_dining_hall():
    dining_hall = request.json['diningHallData']
    db = get_db_connection()
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

@dining_blueprint.route('/editMenuItem', methods=['PUT'])
def edit_menu_item():
    menu_item = request.json['menuItem']
    db = get_db_connection()
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

@dining_blueprint.route('/deleteMenuItem/<int:menu_item_id>', methods=['DELETE'])
def delete_menu_item(menu_item_id):
    # print('MENU_ITEM_ID: ', menu_item_id)
    db = get_db_connection()
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

@dining_blueprint.route('/addMenuItem' , methods=['POST'])
def add_menu_item():
    menu_item = request.json['menuItem']
    db = get_db_connection()
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