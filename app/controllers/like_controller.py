from flask import Blueprint, request, jsonify
from ..services.like_service import LikeService

like_blueprint = Blueprint('like_blueprint', __name__)

class LikeController:
    def __init__(self, like_service: LikeService):
        self.like_service = like_service

    @like_blueprint.route('/like', methods=['POST'])
    def like(self):
        like_data = request.json['likeInfo']
        try:
            response = self.like_service.toggle_like(like_data)
            return jsonify(response), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400   
        except Exception as e:
            return jsonify({'message': str(e)}), 500