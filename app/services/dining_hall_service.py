from ..models.dining_hall import DiningHall
from ..models.restaurant import Restaurant
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
    
    def get_dining_halls_with_restaurants(self):
        raw_dining_halls = self.dining_hall_dao.get_all_dining_halls()
        result = []

        for raw_dining_hall in raw_dining_halls:
            
            dining_hall = DiningHall(
                id=raw_dining_hall[0],
                name=raw_dining_hall[1],
                address=raw_dining_hall[2],
                overall_rating=raw_dining_hall[3],
                description=raw_dining_hall[4]
            )

            raw_restaurants = self.dining_hall_dao.get_restaurants_by_dining_hall(dining_hall.id)

            restaurants_list = [
                Restaurant(
                    id=r[0],
                    name=r[1],
                    overall_rating=r[2],
                    description=r[3],
                    menu_name=r[4],
                    menu_description=r[5],
                    dining_hall_id=r[6]
                ).to_dict() for r in raw_restaurants
            ]

            result.append({
                'dining_hall': dining_hall.to_dict(),
                'restaurants': restaurants_list
            })

        return result
            