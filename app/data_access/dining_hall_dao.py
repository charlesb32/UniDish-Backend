from app.data_access.dining_hall_dao_interface import IDiningHallDAO

class DiningHallDAO(IDiningHallDAO):
    def __init__(self, db_connection):
        self.db = db_connection

    def add_dining_hall(self, dining_hall):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                'INSERT INTO dining_halls (dining_hall_name, description, dining_hall_address) VALUES (%s, %s, %s)',
                (dining_hall.name, dining_hall.description, dining_hall.address)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_dining_hall(self, dining_hall_id):
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM dining_halls WHERE dining_hall_id = %s", (dining_hall_id,))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
    
    def update_dining_hall(self, dining_hall):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "UPDATE dining_halls SET dining_hall_name = %s, description = %s, dining_hall_address = %s WHERE dining_hall_id=%s", 
                (dining_hall.name, dining_hall.description, dining_hall.address, dining_hall.id)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()