class Restaurant:
    def __init__(self, name, description, dining_hall_id, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.dining_hall_id = dining_hall_id

    def __repr__(self):
        return f"<Restaurant {self.name}>"
