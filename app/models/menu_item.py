# models/menu_item.py
class MenuItem:
    def __init__(self, name, description, calories, price, restaurant_id, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.calories = calories
        self.price = price
        self.restaurant_id = restaurant_id

    def to_dict(self):
        """Convert the MenuItem object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'price': self.price,
            'restaurant_id': self.restaurant_id
        }
