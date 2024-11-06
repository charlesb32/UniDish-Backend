# models/review.py
class Review:
    def __init__(self, date, rating, description, restaurant_id, user_id, id=None):
        self.id = id
        self.date = date
        self.rating = rating
        self.description = description
        self.restaurant_id = restaurant_id
        self.user_id = user_id

    def to_dict(self):
        return {
            "review_id": self.review_id,
            "date": self.date,
            "rating": self.rating,
            "description": self.description,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id
        }
