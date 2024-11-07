from app.services.like_service_interface import ILikeService
from app.data_access.like_dao_interface import ILikeDAO
from ..models.like import Like

class LikeService(ILikeService):
    def __init__(self, like_dao: ILikeDAO):
        self.like_dao = like_dao

    def toggle_like(self, like_data):
        if not like_data.get('userId'):
            raise ValueError("Like user id is required")
        if not like_data.get('postId'):
            raise ValueError("Like post id is required")
        if not like_data.get('likeType'):
            raise ValueError("Like type is required")
        
        like = Like(
            user_id=like_data["userId"],
            post_id=like_data["postId"],
            like_type=like_data["likeType"]
        )

        if self.like_dao.has_existing_like(like):
            print("service has like")
            # If already liked, remove the like
            self.like_dao.delete_like(like)
            return {"message": "Review unliked"}
        
        if self.like_dao.has_existing_dislike(like):
            print("service has dislike")
            # If disliked, remove the dislike first
            self.like_dao.delete_dislike(like)
        
        # Add the new like
        self.like_dao.add_like(like)
        return {"message": "Like added successfully"}
