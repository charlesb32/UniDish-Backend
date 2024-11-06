class Restaurant:
    def __init__(self, name, description, dining_hall_id, id=None, overall_rating=None, menu_name=None, menu_description=None):
        self.id = id
        self.name = name
        self.description = description
        self.dining_hall_id = dining_hall_id
        self.overall_rating = overall_rating
        self.menu_name = menu_name
        self.menu_description = menu_description
        
    def to_dict(self):
        """Convert the Restaurant object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'overall_rating': self.overall_rating,
            'description': self.description,
            'menu_name': self.menu_name,
            'menu_description': self.menu_description,
            'dining_hall_id': self.dining_hall_id
        }
        
    def __repr__(self):
        return f"<Restaurant id: {self.id}, name: {self.name}, description: {self.description}, dining_hall_id: {self.dining_hall_id}, overall rating: {self.overall_rating}, menu name: {self.menu_name}, menu description: {self.menu_description}>"