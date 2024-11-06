from typing import List
from ..models.menu_item import MenuItem
from abc import ABC, abstractmethod

class IMenuItemDAO(ABC):
    @abstractmethod
    def add_menu_item(self, menu_item: MenuItem):
        pass
    
    @abstractmethod
    def update_menu_item(self, menu_item: MenuItem):
        pass

    @abstractmethod
    def delete_menu_item(self, menu_item_id: int):
        pass

    @abstractmethod
    def get_menu_items_for_restaurant(self, restaurant_id: int):
        pass