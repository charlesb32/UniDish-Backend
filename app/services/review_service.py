from ..models.review import Review
from app.services.review_service_interface import IReviewService
from app.data_access.review_dao_interface import IReviewDAO

class ReviewService(IReviewService):
    def __init__(self, review_dao: IReviewDAO):
        self.review_dao = review_dao

    def add_review(self, review_data):
        # print(review_data)
        if not review_data.get('restaurantId'):
            raise ValueError("Review restaurant id is required")
        if not review_data.get('userId'):
            raise ValueError("Review user id is required")

        review = Review(
            date=review_data['date'],
            rating=review_data['rating'],
            description=review_data['description'],
            user_id=review_data['userId'],
            restaurant_id=review_data['restaurantId']
        )

        self.review_dao.add_review(review)
    
    def get_reviews(self, restaurant_id: int):
        if not restaurant_id:
            raise ValueError('Reviews restaurant id is required')
        