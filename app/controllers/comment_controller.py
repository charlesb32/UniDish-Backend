from flask import Blueprint, jsonify, request
from ..services.comment_service_interface import ICommentService

comment_blueprint = Blueprint('comment_blueprint', __name__)

class CommentController:
    def __init__(self, comment_service: ICommentService):
        self.comment_service = comment_service

    @comment_blueprint.route('/addComment', methods=['POST'])
    def add_comment(self):
        try:
            comment_data = request.json['commentInfo']
            self.comment_service.add_comment(comment_data)
            return jsonify({"message": "Comment added successfully"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500