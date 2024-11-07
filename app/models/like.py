class Like:
    def __init__(self, user_id, post_id, like_type):
        self.user_id = user_id
        self.post_id = post_id
        self.like_type = like_type  # Can be 'review' or 'comment'
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "like_type": self.like_type
        }
