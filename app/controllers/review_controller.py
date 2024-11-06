from flask import Blueprint, jsonify, request
from ..services.review_service_interface import IReviewService

review_blueprint = Blueprint('review_blueprint', __name__)

class ReviewController:
    def __init__(self, review_service: IReviewService):
        self.review_service = review_service

    @review_blueprint.route('/addReview', methods=['POST'])
    def add_review(self):
        try:
            review_data = request.json['reviewInfo']
            self.review_service.add_review(review_data)
            return jsonify({"message": "Review added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500