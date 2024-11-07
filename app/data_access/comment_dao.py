from app.data_access.comment_dao_interface import ICommentDAO
from app.models.comment import Comment

class CommentDAO(ICommentDAO):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def add_comment(self, comment: Comment):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
        INSERT INTO comments (description, user_id, review_id, date)
        VALUES (%s, %s, %s, %s)
        """, (comment.description, comment.user_id, comment.review_id, comment.date))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()  