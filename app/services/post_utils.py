import mysql.connector
from .database import get_db_connection

def get_review_likes(post_id, post_type):
    # print('POST ID: ', post_id)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = ''
        if post_type == 'review':
            query = """
            SELECT COUNT(*) AS likes_count
            FROM review_likes
            WHERE rreview_id = %s
            """
        elif post_type == 'comment':
            query = """
            SELECT COUNT(*) AS likes_count
            FROM comment_likes
            WHERE ccomment_id = %s
            """
        cursor.execute(query, (post_id,))
        result = cursor.fetchone()  # Fetch the result
        return result['likes_count'] if result else 0
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_review_dislikes(post_id, post_type):
    # print('POST ID: ', post_id)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = ''
        if post_type == 'review':
            query = """
            SELECT COUNT(*) AS dislikes_count
            FROM review_dislikes
            WHERE rreview_id = %s
            """
        elif post_type == 'comment':
            query = """
            SELECT COUNT(*) AS dislikes_count
            FROM comment_dislikes
            WHERE ccomment_id = %s
            """
        cursor.execute(query, (post_id,))
        result = cursor.fetchone()  # Fetch the result
        return result['dislikes_count'] if result else 0
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_user(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
        SELECT * 
        FROM users
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  # Fetch the result
        # print('USER: ', result)
        return result
    except Exception as e:
        # print(f"Error getting likes: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()

def get_highlight(user_id, post_id, post_type):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    # print('USER AND POST IDS', user_id, post_id)
    try:
        like_query = ''
        dislike_query = ''
        if post_type == 'review':
            like_query = """
            SELECT * FROM review_likes
            WHERE uuser_id = %s AND rreview_id = %s
            """
            cursor.execute(like_query, (user_id, post_id))
            like_result = cursor.fetchone()  # Fetch the result
            # print('LIKE_RESULT: ',like_result)
            if like_result:
                return 'like'
            dislike_query = """
            SELECT * FROM review_dislikes
            WHERE uuser_id = %s AND rreview_id = %s
            """
            cursor.execute(dislike_query, (user_id, post_id))
            dislike_result = cursor.fetchone()  # Fetch the result
            if dislike_result:
                return 'dislike'
        elif post_type == 'comment':
            like_query = """
            SELECT * FROM comment_likes
            WHERE uuser_id = %s AND ccomment_id = %s
            """
            cursor.execute(like_query, (user_id, post_id))
            like_result = cursor.fetchone()  # Fetch the result
            # print('LIKE_RESULT: ',like_result)
            if like_result:
                return 'like'
            dislike_query = """
            SELECT * FROM comment_dislikes
            WHERE uuser_id = %s AND ccomment_id = %s
            """
            cursor.execute(dislike_query, (user_id, post_id))
            dislike_result = cursor.fetchone()  # Fetch the result
            if dislike_result:
                return 'dislike'
        return ''
    except Exception as e:
        # print(f"Error getting highlight info: {e}")  # Properly log the exception or handle it.
        return 0
    finally:
        cursor.close()
        db.close()