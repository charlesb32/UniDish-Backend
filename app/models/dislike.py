class Dislike:
    def __init__(self, user_id, post_id, dislike_type):
        self.user_id = user_id
        self.post_id = post_id
        self.dislike_type = dislike_type  # Can be 'review' or 'comment'

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "dislike_type": self.dislike_type
        }
