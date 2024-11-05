# controllers/dining_hall_controller.py
from flask import Blueprint, jsonify, request
from ..services.restaurant_service import RestaurantService
# from ..data_access.restaurant_dao import RestaurantDAO
# from ..services.database import get_db_connection
from ..services.restaurant_service_interface import IRestaurantService

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__)

class RestaurantController:
    def __init__(self, restaurant_service: IRestaurantService):
        self.restaurant_service = restaurant_service

    @restaurant_blueprint.route('/addRestaurant', methods=['POST'])
    def add_restaurant(self):
        # db = get_db_connection()
        # restaurant_dao = RestaurantDAO(db)
        # restaurant_service = RestaurantService(restaurant_dao)

        try:
            restaurant_data = request.json['restData']
            self.restaurant_service.add_restaurant(restaurant_data)
            return jsonify({"message": "Restaurant added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        # finally:
        #     db.close()  # Ensure the DB connection is closed after the operation


    @restaurant_blueprint.route('/deleteRestaurant/<int:restaurant_id>', methods=['DELETE'])
    def delete_restaurant(self, restaurant_id):
        print('controller')
        # db = get_db_connection()
        # restaurant_dao = RestaurantDAO(db)
        # restaurant_service = RestaurantService(restaurant_dao)

        try:
            self.restaurant_service.delete_restaurant(restaurant_id)
            return jsonify({"message": "Restaurant deleted successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        # finally:
        #     db.close()  # Ensure the DB connection is closed after the operation

    @restaurant_blueprint.route('/updateRestaurant', methods=['PUT'])
    def edit_restaurant(self):
        # db = get_db_connection()
        # restaurant_dao = RestaurantDAO(db)
        # restaurant_service = RestaurantService(restaurant_dao)

        try:
            restaurant_data = request.json['restData']
            self.restaurant_service.update_restaurant(restaurant_data)
            return jsonify({"message": "Restaurant updated successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        # finally:
        #     db.close()  # Ensure the DB connection is closed after the operation