from ..models.menu_item import MenuItem
from app.data_access.menu_item_dao_interface import IMenuItemDAO

class MenuItemDAO(IMenuItemDAO):
    def __init__(self, db_connection):
        self.db = db_connection

    def add_menu_item(self, menu_item: MenuItem):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                'INSERT INTO menu_items (name, description, calorie_count, price, restaurant_id) VALUES (%s, %s, %s, %s, %s)',
                (menu_item.name, menu_item.description, menu_item.calories, menu_item.price, menu_item.restaurant_id)
            )
            self.db.commit()
        finally:
            cursor.close()

    def update_menu_item(self, menu_item: MenuItem):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "UPDATE menu_items SET name = %s, description = %s, calorie_count = %s, price = %s WHERE menu_item_id= %s",
                (menu_item.name, menu_item.description, menu_item.calories, menu_item.price, menu_item.id)
            )
            self.db.commit()
        finally:
            cursor.close()

    def delete_menu_item(self, menu_item_id: int):
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM menu_items WHERE menu_item_id = %s", (menu_item_id,))
            self.db.commit()
        finally:
            cursor.close()

    def get_menu_items_for_restaurant(self, restaurant_id: int):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM menu_items WHERE restaurant_id = %s", (restaurant_id,))
            return cursor.fetchall()
        finally:
            cursor.close()