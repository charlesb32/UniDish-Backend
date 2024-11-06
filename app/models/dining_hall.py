
class DiningHall:
    def __init__(self, name, description, address, id=None, overall_rating=None):
        self.id = id
        self.name = name
        self.description = description
        self.address = address
        self.overall_rating = overall_rating

    def to_dict(self):
        """Convert the DiningHall object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'overall_rating': self.overall_rating,
            'description': self.description
        }

    def __repr__(self):
        return f"<DiningHall id: {self.id}, name:{self.name}, address: {self.address}, overall rating: {self.overall_rating}, description: {self.description}>"