from flask import Blueprint, jsonify, request
from ..services.restaurant_service_interface import IRestaurantService

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__)

class RestaurantController:
    def __init__(self, restaurant_service: IRestaurantService):
        self.restaurant_service = restaurant_service

    @restaurant_blueprint.route('/addRestaurant', methods=['POST'])
    def add_restaurant(self):
        try:
            restaurant_data = request.json['restData']
            self.restaurant_service.add_restaurant(restaurant_data)
            return jsonify({"message": "Restaurant added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @restaurant_blueprint.route('/deleteRestaurant/<int:restaurant_id>', methods=['DELETE'])
    def delete_restaurant(self, restaurant_id):
        try:
            self.restaurant_service.delete_restaurant(restaurant_id)
            return jsonify({"message": "Restaurant deleted successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @restaurant_blueprint.route('/updateRestaurant', methods=['PUT'])
    def edit_restaurant(self):
        try:
            restaurant_data = request.json['restData']
            self.restaurant_service.update_restaurant(restaurant_data)
            return jsonify({"message": "Restaurant updated successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @restaurant_blueprint.route('/getRestaurant/<int:restaurant_id>', methods=['GET'])
    def get_restaurant(self, restaurant_id):
        try:
            restaurant = self.restaurant_service.get_restaurant(restaurant_id)
            return jsonify({'restaurant': restaurant}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @restaurant_blueprint.route('/getOverallRestaurantRating/<int:restaurant_id>', methods=['GET'])
    def get_overall_restaurant_rating(self, restaurant_id):
        try:
            average_rating = self.restaurant_service.get_average_rating(restaurant_id)
            return jsonify({'averageRating': average_rating}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500