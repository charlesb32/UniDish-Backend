# controllers/dining_hall_controller.py
from flask import Blueprint, jsonify, request
from ..services.dining_hall_service import DiningHallService
from ..data_access.dining_hall_dao import DiningHallDAO
from ..services.database import get_db_connection

dining_hall_blueprint = Blueprint('dining_hall_blueprint', __name__)

@dining_hall_blueprint.route('/addDiningHall', methods=['POST'])
def add_dining_hall():
    db = get_db_connection()  # Get DB connection from connection pool
    dining_hall_dao = DiningHallDAO(db)
    dining_hall_service = DiningHallService(dining_hall_dao)

    try:
        dining_hall_data = request.json['diningHallData']
        dining_hall_service.add_dining_hall(dining_hall_data)
        return jsonify({"message": "Dining Hall added successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure connection is closed after the transaction


@dining_hall_blueprint.route('/deleteDiningHall/<int:dining_hall_id>', methods=["DELETE"])
def delete_dining_hall(dining_hall_id):
    db = get_db_connection()  # Get DB connection from connection pool
    dining_hall_dao = DiningHallDAO(db)
    dining_hall_service = DiningHallService(dining_hall_dao)

    try:
        dining_hall_service.delete_dining_hall(dining_hall_id)
        return jsonify({"message": "Dining hall deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure the DB connection is closed after the operation

@dining_hall_blueprint.route('/updateDiningHall', methods=['PUT'])
def edit_dining_hall():
    db = get_db_connection()  # Get DB connection from connection pool
    dining_hall_dao = DiningHallDAO(db)
    dining_hall_service = DiningHallService(dining_hall_dao)

    try:
        dining_hall_data = request.json['diningHallData']
        dining_hall_service.update_dining_hall(dining_hall_data)
        return jsonify({"message": "Dining Hall updated successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure the DB connection is closed after the operation