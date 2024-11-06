# controllers/menu_item_controller.py
from flask import Blueprint, request, jsonify
from ..services.menu_item_service_interface import IMenuItemService

menu_item_blueprint = Blueprint('menu_item_blueprint', __name__)

class MenuItemController:
    def __init__(self, menu_item_service: IMenuItemService):
        self.menu_item_service = menu_item_service

    @menu_item_blueprint.route('/addMenuItem', methods=['POST'])
    def add_menu_item(self):
        menu_item_data = request.json['menuItem']
        try:
            self.menu_item_service.add_menu_item(menu_item_data)
            return jsonify({"message": "Menu Item Added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    @menu_item_blueprint.route('/editMenuItem', methods=['PUT'])
    def edit_menu_item(self):
        menu_item_data = request.json['menuItem']
        try:
            self.menu_item_service.update_menu_item(menu_item_data)
            return jsonify({"message": "Menu Item Updated successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    @menu_item_blueprint.route('/deleteMenuItem/<int:menu_item_id>', methods=['DELETE'])
    def delete_menu_item(self, menu_item_id):
        try:
            self.menu_item_service.delete_menu_item(menu_item_id)
            return jsonify({"message": "Menu Item Deleted successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    @menu_item_blueprint.route('/getMenuItemsForRestaurant/<int:restaurant_id>', methods=['GET'])
    def get_menu_items_for_restaurant(self, restaurant_id):
        try:
            menu_items = self.menu_item_service.get_menu_items_for_restaurant(restaurant_id)
            return jsonify({'menu_items': menu_items}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500
