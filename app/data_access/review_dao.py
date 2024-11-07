from app.data_access.review_dao_interface import IReviewDAO

class ReviewDAO(IReviewDAO):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def add_review(self, review):
        cursor = self.db.cursor()
        try:
            cursor.execute(
            'INSERT INTO reviews (date, rating, description, restaurant_id, user_id) VALUES (%s, %s, %s, %s, %s)',
            (review.date, review.rating, review.description, review.restaurant_id, review.user_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()
    
    # def get_reviews(self, restaurant_id: int):
    #     cursor = self.db.cursor()
    #     try:
            