from app.data_access.like_dao_interface import ILikeDAO
from app.models.like import Like
class LikeDAO(ILikeDAO):
    def __init__(self, db_connection):
        self.db = db_connection

    def has_existing_like(self, like: Like):
        cursor = self.db.cursor(dictionary=True)
        try:
            table = "review_likes" if like.like_type == "review" else "comment_likes"
            query = f"SELECT COUNT(*) AS like_count FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if like.like_type == "review" else f"SELECT COUNT(*) AS like_count FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (like.user_id, like.post_id))
            print('TABLE: ', table, "query: ", query, "userID: ", like.user_id, "postID: ", like.post_id)
            print(cursor)
            test =  cursor.fetchone()["like_count"]
            print(test)
            # return cursor.fetchone()["like_count"] > 0
            return test
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def add_like(self, like: Like):
        cursor = self.db.cursor()
        try:
            table = "review_likes" if like.like_type == "review" else "comment_likes"
            query = f"INSERT INTO {table} (uuser_id, rreview_id) VALUES (%s, %s)" if like.like_type == "review" else f"INSERT INTO {table} (uuser_id, ccomment_id) VALUES (%s, %s)"
            cursor.execute(query, (like.user_id, like.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e    
        finally:
            cursor.close()

    def delete_like(self, like: Like):
        cursor = self.db.cursor()
        try:
            table = "review_likes" if like.like_type == "review" else "comment_likes"
            query = f"DELETE FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if like.like_type == "review" else f"DELETE FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (like.user_id, like.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e    
        finally:
            cursor.close()

    def has_existing_dislike(self, like: Like):
        cursor = self.db.cursor(dictionary=True)
        try:
            table = "review_dislikes" if like.like_type == "review" else "comment_dislikes"
            query = f"SELECT COUNT(*) AS dislike_count FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if like.like_type == "review" else f"SELECT COUNT(*) AS dislike_count FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (like.user_id, like.post_id))
            return cursor.fetchone()["dislike_count"] > 0
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            cursor.close()

    def delete_dislike(self, like: Like):
        cursor = self.db.cursor()
        try:
            table = "review_dislikes" if like.like_type == "review" else "comment_dislikes"
            query = f"DELETE FROM {table} WHERE uuser_id = %s AND rreview_id = %s" if like.like_type == "review" else f"DELETE FROM {table} WHERE uuser_id = %s AND ccomment_id = %s"
            cursor.execute(query, (like.user_id, like.post_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e    
        finally:
            cursor.close()
