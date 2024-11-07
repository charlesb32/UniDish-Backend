from ..models.restaurant import Restaurant
from app.services.restaurant_service_interface import IRestaurantService
from app.data_access.restaurant_dao_interface import IRestaurantDAO

class RestaurantService(IRestaurantService):
    def __init__(self, restaurant_dao: IRestaurantDAO):
        self.restaurant_dao = restaurant_dao

    def add_restaurant(self, restaurant_data):
        if not restaurant_data.get('name'):
            raise ValueError("Restaurant name is required")
        if not restaurant_data.get('diningHallId'):
            raise ValueError("Dining hall ID is required")

        restaurant = Restaurant(
            name=restaurant_data['name'],
            description=restaurant_data['description'],
            dining_hall_id=restaurant_data['diningHallId']
        )

        self.restaurant_dao.add_restaurant(restaurant)

    def delete_restaurant(self, restaurant_id):
        if not restaurant_id:
            raise ValueError("Restaurant ID is required")

        self.restaurant_dao.delete_restaurant(restaurant_id)
    
    def update_restaurant(self, restaurant_data):
        if not restaurant_data.get('id'):
            raise ValueError("Restaurant ID is required")
        if not restaurant_data.get('name'):
            raise ValueError("Restaurant name is required")

        restaurant = Restaurant(
            id=restaurant_data['id'],
            name=restaurant_data['name'],
            description=restaurant_data['description'],
            dining_hall_id=restaurant_data['diningHallId']
        )

        self.restaurant_dao.update_restaurant(restaurant)

    def get_restaurant(self, restaurant_id: int):
        if not restaurant_id:
            raise ValueError("Restaurant ID is required")

        restaurant = self.restaurant_dao.get_restaurant(restaurant_id)
        if restaurant is None:
            raise ValueError(f"Restaurant with ID {restaurant_id} not found")
        
        return restaurant
    
    def get_average_rating(self, restaurant_id: int):
        if not restaurant_id:
            raise ValueError("Restaurant ID is required")

        average_rating = self.restaurant_dao.get_average_rating(restaurant_id)
        if average_rating is None:
            raise ValueError(f"Restaurant with ID {restaurant_id} not found")

        return average_rating