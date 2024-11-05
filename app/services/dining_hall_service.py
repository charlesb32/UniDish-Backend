from ..models.dining_hall import DiningHall
from app.services.dining_hall_service_interface import IDiningHallService
from app.data_access.dining_hall_dao_interface import IDiningHallDAO

class DiningHallService(IDiningHallService):
    def __init__(self, dining_hall_dao: IDiningHallDAO):
        self.dining_hall_dao = dining_hall_dao

    def add_dining_hall(self, dining_hall_data):
        if not dining_hall_data.get('name') or not dining_hall_data.get('address'):
            raise ValueError("Dining hall name and address are required")

        dining_hall = DiningHall(
            name=dining_hall_data['name'],
            description=dining_hall_data['description'],
            address=dining_hall_data['address']
        )

        self.dining_hall_dao.add_dining_hall(dining_hall)

    def delete_dining_hall(self, dining_hall_id):
        if not dining_hall_id:
            raise ValueError("Dining hall ID is required")

        self.dining_hall_dao.delete_dining_hall(dining_hall_id)
    
    def update_dining_hall(self, dining_hall_data):
        if not dining_hall_data.get('id'):
            raise ValueError("Dining hall ID is required")
        if not dining_hall_data.get('name'):
            raise ValueError("Dining hall name is required")

        dining_hall = DiningHall(
            id=dining_hall_data['id'],
            name=dining_hall_data['name'],
            description=dining_hall_data['description'],
            address=dining_hall_data['address']
        )

        self.dining_hall_dao.update_dining_hall(dining_hall)