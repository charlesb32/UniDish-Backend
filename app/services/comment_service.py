from ..models.comment import Comment
from app.services.comment_service_interface import ICommentService
from app.data_access.comment_dao_interface import ICommentDAO

class CommentService(ICommentService):
    def __init__(self, comment_dao: ICommentDAO):
        self.comment_dao = comment_dao

    def add_comment(self, comment_data):
        print('COMMETN DATA SERVICE: ', comment_data)
        if not comment_data.get('userId'):
            raise ValueError("Comment user id is required")
        if not comment_data.get('reviewId'):
            raise ValueError("Comment review id is required")

        comment = Comment(
            date=comment_data['date'],
            description=comment_data['description'],
            user_id=comment_data['userId'],
            review_id=comment_data['reviewId']
        )

        self.comment_dao.add_comment(comment)