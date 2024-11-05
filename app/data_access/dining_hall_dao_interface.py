from abc import ABC, abstractmethod
from ..models.dining_hall import DiningHall

class IDiningHallDAO(ABC):
    @abstractmethod
    def add_dining_hall(self, dining_hall: DiningHall):
        pass

    @abstractmethod
    def delete_dining_hall(self, dining_hall_id: int):
        pass

    @abstractmethod
    def update_dining_hall(self, dining_hall: DiningHall):
        pass
    
    @abstractmethod
    def get_all_dining_halls(self):
        pass
    
    @abstractmethod
    def get_restaurants_by_dining_hall(self, dining_hall_id):
        pass