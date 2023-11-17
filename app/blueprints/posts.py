from flask import Blueprint, jsonify, request
from ..services.post_utils import get_review_likes, get_review_dislikes, get_user, get_highlight
from ..services.database import get_db_connection

posts_blueprint = Blueprint('posts', __name__)

@posts_blueprint.route('/getReviews', methods=['GET'])
def get_reviews_and_review_info():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        rest_id = request.args.get('restId')
        # print('REST_ID: ', rest_id)
        curr_user_id = request.args.get('currUserId')
        # print('CURRUSERID: ', curr_user_id)
        query = """
        SELECT * FROM reviews 
        WHERE restaurant_id = %s 
        ORDER BY date DESC
        """
        cursor.execute(query, (rest_id,))  # Note the comma for a single parameter
        reviews = cursor.fetchall()
        for review in reviews:
            review['likes'] = get_review_likes(review['review_id'], 'review')
            review['dislikes'] = get_review_dislikes(review['review_id'], 'review')
            review['user'] = get_user(review['user_id'])
            review['highlight'] = get_highlight(curr_user_id, review['review_id'], 'review')
        # print('REVIEWS: ', reviews)
        cursor.close()
        db.close()
        return jsonify(reviews)
    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({'message': str(e)}), 500

@posts_blueprint.route('/like', methods=['POST'])
def add_like():
    like_info = request.json['likeInfo']
    # print(like_info)
    user_id = like_info['userId']
    post_id = like_info['postId']
    like_type = like_info['likeType']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if like_type == 'review':
        # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM review_likes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            like_result = cursor.fetchone()

            if like_result['like_count'] > 0:
                #if already liked remove the like
                cursor.execute("""
                    DELETE FROM review_likes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review unliked'}), 200
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM review_dislikes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['dislike_count'] > 0:
                # User has disliked the review, remove the dislike
                cursor.execute("""
                    DELETE FROM review_dislikes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
            # Now add the like (after removing dislike if it was there)
            cursor.execute("""
                INSERT INTO review_likes (uuser_id, rreview_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        elif like_type == 'comment':
        # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM comment_likes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            like_result = cursor.fetchone()

            if like_result['like_count'] > 0:
                #if already liked remove the like
                cursor.execute("""
                    DELETE FROM comment_likes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review unliked'}), 200
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM comment_dislikes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['dislike_count'] > 0:
                # User has disliked the review, remove the dislike
                cursor.execute("""
                    DELETE FROM comment_dislikes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
            # Now add the like (after removing dislike if it was there)
            cursor.execute("""
                INSERT INTO comment_likes (uuser_id, ccomment_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        return jsonify({'message': 'Like added successfully'}), 200

    except Exception as e:
        db.rollback()
        # print(f"Error in add_like: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@posts_blueprint.route('/dislike', methods=['POST'])
def add_dislike():
    dislike_info = request.json['dislikeInfo']
    # print(dislike_info)
    user_id = dislike_info['userId']
    post_id = dislike_info['postId']
    dislike_type = dislike_info['dislikeType']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if dislike_type == 'review':
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM review_dislikes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            dislike_result = cursor.fetchone()

            if dislike_result['dislike_count'] > 0:
                # User has already disliked the review, remove dislike
                cursor.execute("""
                    DELETE FROM review_dislikes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review undisliked'}), 200
            # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM review_likes
                WHERE uuser_id = %s AND rreview_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['like_count'] > 0:
                # User has liked the review, remove the like
                cursor.execute("""
                    DELETE FROM review_likes
                    WHERE uuser_id = %s AND rreview_id = %s
                """, (user_id, post_id))
                db.commit()

            # Now add the dislike (after removing like if it was there)
            cursor.execute("""
                INSERT INTO review_dislikes (uuser_id, rreview_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        elif dislike_type == 'comment':
            # Check if the user has already disliked this review
            cursor.execute("""
                SELECT COUNT(*) AS dislike_count
                FROM comment_dislikes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            dislike_result = cursor.fetchone()

            if dislike_result['dislike_count'] > 0:
                # User has already disliked the review, remove dislike
                cursor.execute("""
                    DELETE FROM comment_dislikes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()
                return jsonify({'message': 'Review undisliked'}), 200
            # Check if the user has already liked this review
            cursor.execute("""
                SELECT COUNT(*) AS like_count
                FROM comment_likes
                WHERE uuser_id = %s AND ccomment_id = %s
            """, (user_id, post_id))
            result = cursor.fetchone()
            
            if result['like_count'] > 0:
                # User has liked the review, remove the like
                cursor.execute("""
                    DELETE FROM comment_likes
                    WHERE uuser_id = %s AND ccomment_id = %s
                """, (user_id, post_id))
                db.commit()

            # Now add the dislike (after removing like if it was there)
            cursor.execute("""
                INSERT INTO comment_dislikes (uuser_id, ccomment_id)
                VALUES (%s, %s)
            """, (user_id, post_id))
            db.commit()
        return jsonify({'message': 'Dislike added successfully'}), 200

    except Exception as e:
        db.rollback()
        # print(f"Error in add_like: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@posts_blueprint.route('/getOverallRestaurantRating', methods=['GET'])
def get_overall_restaurant_rating():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    rest_id = request.args.get('restId')
    # print('REST_ID:!!!!!!!!! ', rest_id)
    try:
        query = "SELECT AVG(rating) as average_rating FROM reviews WHERE restaurant_id = %s"
        cursor.execute(query, (rest_id,))
        result = cursor.fetchone()
        average_rating = result['average_rating'] if result['average_rating'] is not None else 0
        return jsonify({'averageRating': average_rating}), 200
        
    except Exception as e:
        db.rollback()
        # print(f"Error in get_overall_restaurant_rating: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@posts_blueprint.route('/createReview', methods=['POST'])
def create_review():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    review_info = request.json['reviewInfo']
    rating = review_info['rating']
    description = review_info['description']
    user_id = review_info['userId']
    rest_id = review_info['restaurantId']
    date = review_info['date']
    try:
        cursor.execute("""
        INSERT INTO reviews (date, rating, description, restaurant_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (date, rating, description, rest_id, user_id))
        db.commit()
        return jsonify({'message': 'Review added successfully'}), 200
    except Exception as e:
        # print(f"Error in create_review: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@posts_blueprint.route('/createComment', methods=['POST'])
def create_comment():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    comment_info = request.json['commentInfo']
    description = comment_info['description']
    user_id = comment_info['userId']
    date = comment_info['date']
    review_id = comment_info['reviewId']
    try:
        cursor.execute("""
        INSERT INTO comments (description, user_id, review_id, date)
        VALUES (%s, %s, %s, %s)
        """, (description, user_id, review_id, date))
        db.commit()
        return jsonify({'message': 'Comment added successfully'}), 200
    except Exception as e:
        # print(f"Error in create_comment: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()

@posts_blueprint.route('/getComments', methods=['GET'])
def get_review_comments():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    review_id = request.args.get('reviewId')
    curr_user_id = request.args.get('currUserId')
    # print('REST_ID:!!!!!!!!! ', rest_id)
    try:
        query = "SELECT * FROM comments WHERE review_id = %s ORDER BY date DESC"
        cursor.execute(query, (review_id,))
        comments = cursor.fetchall()
        for comment in comments:    
            comment['likes'] = get_review_likes(comment['comment_id'], 'comment')
            comment['dislikes'] = get_review_dislikes(comment['comment_id'], 'comment')
            comment['user'] = get_user(comment['user_id'])
            comment['highlight'] =  get_highlight(curr_user_id, comment['comment_id'], 'comment')
            # print('COMMENTS: ', comments)
        return jsonify({'comment': comments}), 200
        
    except Exception as e:
        # print(f"Error in get_review_comments: {e}")
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        db.close()
