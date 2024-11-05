from flask import Blueprint, jsonify, request
from ..services.dining_hall_service_interface import IDiningHallService

dining_hall_blueprint = Blueprint('dining_hall_blueprint', __name__)

class DiningHallController:
    def __init__(self, dining_hall_service: IDiningHallService):
        self.dining_hall_service = dining_hall_service

    @dining_hall_blueprint.route('/addDiningHall', methods=['POST'])
    def add_dining_hall(self):
        try:
            dining_hall_data = request.json['diningHallData']
            self.dining_hall_service.add_dining_hall(dining_hall_data)
            return jsonify({"message": "Dining Hall added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @dining_hall_blueprint.route('/deleteDiningHall/<int:dining_hall_id>', methods=["DELETE"])
    def delete_dining_hall(self, dining_hall_id):
        try:
            self.dining_hall_service.delete_dining_hall(dining_hall_id)
            return jsonify({"message": "Dining hall deleted successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @dining_hall_blueprint.route('/updateDiningHall', methods=['PUT'])
    def edit_dining_hall(self):
        try:
            dining_hall_data = request.json['diningHallData']
            self.dining_hall_service.update_dining_hall(dining_hall_data)
            return jsonify({"message": "Dining Hall updated successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @dining_hall_blueprint.route('/getDiningHallsWithRestaurants', methods=['GET'])
    def get_dining_halls_with_restaurants(self):
        try:
            dining_halls_with_restaurants = self.dining_hall_service.get_dining_halls_with_restaurants()
            return jsonify({'dining_halls': dining_halls_with_restaurants}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500