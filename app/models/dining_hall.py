
class DiningHall:
    def __init__(self, name, description, address, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.address = address

    def __repr__(self):
        return f"<DiningHall {self.name}>"
