from app.data_access.restaurant_dao_interface import IRestaurantDAO
# from ..models.restaurant import Restaurant
# from restaurant_dao_interface import IRestaurantDAO

class RestaurantDAO(IRestaurantDAO):
    def __init__(self, db_connection):
        self.db = db_connection

    def add_restaurant(self, restaurant):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                'INSERT INTO restaurants (name, description, dining_hall_id) VALUES (%s, %s, %s)', 
                (restaurant.name, restaurant.description, restaurant.dining_hall_id)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_restaurant(self, restaurant_id):
        print('DAO', restaurant_id)
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM restaurants WHERE restaurant_id = %s", (restaurant_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
    
    def update_restaurant(self, restaurant):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "UPDATE restaurants SET name = %s, description = %s WHERE restaurant_id=%s", 
                (restaurant.name, restaurant.description, restaurant.id)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()