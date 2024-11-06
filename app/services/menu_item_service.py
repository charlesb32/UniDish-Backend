# services/menu_item_service.py
from app.services.menu_item_service_interface import IMenuItemService
from ..data_access.menu_item_dao_interface import IMenuItemDAO
from ..models.menu_item import MenuItem

class MenuItemService(IMenuItemService):
    def __init__(self, menu_item_dao: IMenuItemDAO):
        self.menu_item_dao = menu_item_dao

    def add_menu_item(self, menu_item_data):
        if not menu_item_data.get('name'):
            raise ValueError("Menu Item name is required")
        if not menu_item_data.get('restaurantId'):
            raise ValueError("Menu Item restaurant id is required")
        
        menu_item = MenuItem(
            name=menu_item_data['name'],
            description=menu_item_data['description'],
            calories=menu_item_data['calories'],
            price=menu_item_data['price'],
            restaurant_id=menu_item_data['restaurantId']
        )
        self.menu_item_dao.add_menu_item(menu_item)

    def update_menu_item(self, menu_item_data):
        if not menu_item_data.get('name'):
            raise ValueError("Menu Item name is required")
        if not menu_item_data.get('restaurantId'):
            raise ValueError("Menu Item restaurant id is required")
        if not menu_item_data.get('id'):
            raise ValueError("Menu Item id is required")

        menu_item = MenuItem(
            id=menu_item_data['id'],
            name=menu_item_data['name'],
            description=menu_item_data['description'],
            calories=menu_item_data['calories'],
            price=menu_item_data['price'],
            restaurant_id=menu_item_data['restaurantId']
        )
        self.menu_item_dao.update_menu_item(menu_item)

    def delete_menu_item(self, menu_item_id):
        if not menu_item_id:
            raise ValueError("Menu Item id is required")
        
        self.menu_item_dao.delete_menu_item(menu_item_id)

    def get_menu_items_for_restaurant(self, restaurant_id):
        if not restaurant_id:
            raise ValueError("Menu Item restaurant id is required")
        
        results = []
        raw_menu_items = self.menu_item_dao.get_menu_items_for_restaurant(restaurant_id)
        
        for raw_menu_item in raw_menu_items:
            
            menu_item = MenuItem(
                id=raw_menu_item['menu_item_id'],
                name=raw_menu_item['name'],
                description=raw_menu_item['description'],
                calories=raw_menu_item['calorie_count'],
                price=raw_menu_item['price'],
                restaurant_id=raw_menu_item['restaurant_id']
            )
            results.append(menu_item.to_dict())
            
        return results
