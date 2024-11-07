from app.data_access.restaurant_dao_interface import IRestaurantDAO

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
    
    def get_restaurant(self, restaurant_id):
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM restaurants WHERE restaurant_id=%s", (restaurant_id,))
            restaurant = cursor.fetchone()
            return restaurant
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
    
    def get_average_rating(self, restaurant_id: int):
        cursor = self.db.cursor(dictionary=True)
        try:
            query = "SELECT AVG(rating) AS average_rating FROM reviews WHERE restaurant_id = %s"
            cursor.execute(query, (restaurant_id,))
            result = cursor.fetchone()
            return result['average_rating'] if result['average_rating'] else 0
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()