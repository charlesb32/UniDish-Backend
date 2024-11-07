from app.data_access.dislike_dao_interface import IDislikeDAO
from app.models.dislike import Dislike

class DislikeDAO(IDislikeDAO):
    def __init__(self, db_connection):
        self.db = db_connection

    def has_existing_dislike(self, dislike: Dislike):
        cursor = self.db.cursor(dictionary=True)
        try:
            table = "review_dislikes" if dislike.dislike_type == "review" else "comment_dislikes"
            query = f"SELECT COUNT(*) AS dislike_count FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if dislike.dislike_type == "review" else f"SELECT COUNT(*) AS dislike_count FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (dislike.user_id, dislike.post_id))
            return cursor.fetchone()["dislike_count"] > 0
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def add_dislike(self, dislike: Dislike):
        cursor = self.db.cursor()
        try:
            table = "review_dislikes" if dislike.dislike_type == "review" else "comment_dislikes"
            query = f"INSERT INTO {table} (uuser_id, rreview_id) VALUES (%s, %s)" if dislike.dislike_type == "review" else f"INSERT INTO {table} (uuser_id, ccomment_id) VALUES (%s, %s)"
            cursor.execute(query, (dislike.user_id, dislike.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_dislike(self, dislike: Dislike):
        cursor = self.db.cursor()
        try:
            table = "review_dislikes" if dislike.dislike_type == "review" else "comment_dislikes"
            query = f"DELETE FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if dislike.dislike_type == "review" else f"DELETE FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (dislike.user_id, dislike.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def has_existing_like(self, dislike: Dislike):
        cursor = self.db.cursor(dictionary=True)
        try:
            table = "review_likes" if dislike.dislike_type == "review" else "comment_likes"
            query = f"SELECT COUNT(*) AS like_count FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if dislike.dislike_type == "review" else f"SELECT COUNT(*) AS like_count FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (dislike.user_id, dislike.post_id))
            return cursor.fetchone()["like_count"] > 0
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_like(self, dislike: Dislike):
        cursor = self.db.cursor()
        try:
            table = "review_likes" if dislike.dislike_type == "review" else "comment_likes"
            query = f"DELETE FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if dislike.dislike_type == "review" else f"DELETE FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (dislike.user_id, dislike.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e    
        finally:
            cursor.close()
