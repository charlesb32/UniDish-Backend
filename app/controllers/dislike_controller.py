from flask import Blueprint, request, jsonify
from ..services.dislike_service import DislikeService

dislike_blueprint = Blueprint('dislike_blueprint', __name__)

class DislikeController:
    def __init__(self, dislike_service: DislikeService):
        self.dislike_service = dislike_service

    @dislike_blueprint.route('/dislike', methods=['POST'])
    def dislike(self):
        dislike_data = request.json['dislikeInfo']
        try:
            response = self.dislike_service.toggle_dislike(dislike_data)
            return jsonify(response), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400  
        except Exception as e:
            return jsonify({'message': str(e)}), 500