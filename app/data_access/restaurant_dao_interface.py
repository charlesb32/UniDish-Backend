from abc import ABC, abstractmethod
from ..models.restaurant import Restaurant

class IRestaurantDAO(ABC):
    @abstractmethod
    def add_restaurant(self, restaurant: Restaurant):
        pass

    @abstractmethod
    def delete_restaurant(self, restaurant_id: int):
        pass

    @abstractmethod
    def update_restaurant(self, restaurant: Restaurant):
        pass
