class Comment:
    def __init__(self, date, description, user_id, review_id = None, comment_comment_id= None, id=None):
        self.id = id
        self.date = date
        self.description = description
        self.review_id = review_id
        self.user_id = user_id
        self.comment_comment_id = comment_comment_id

    # def to_dict(self):
    #     return {
    #         "review_id": self.review_id,
    #         "date": self.date,
    #         "rating": self.rating,
    #         "description": self.description,
    #         "restaurant_id": self.restaurant_id,
    #         "user_id": self.user_id
    #     }
