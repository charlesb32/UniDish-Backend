from app.services.dislike_service_interface import IDislikeService
from app.data_access.dislike_dao_interface import IDislikeDAO
from ..models.dislike import Dislike

class DislikeService(IDislikeService):
    def __init__(self, dislike_dao: IDislikeDAO):
        self.dislike_dao = dislike_dao

    def toggle_dislike(self, dislike_data):
        print(dislike_data)
        if not dislike_data.get('userId'):
            raise ValueError("Dislike user id is required")
        if not dislike_data.get('postId'):
            raise ValueError("Dislike post id is required")
        if not dislike_data.get('dislikeType'):
            raise ValueError("Dislike type is required")
        
        dislike = Dislike(
            user_id=dislike_data["userId"],
            post_id=dislike_data["postId"],
            dislike_type=dislike_data["dislikeType"]
        )
        
        if self.dislike_dao.has_existing_dislike(dislike):
            # If already disliked, remove the dislike
            self.dislike_dao.delete_dislike(dislike)
            return {"message": "Review undisliked"}
        
        if self.dislike_dao.has_existing_like(dislike):
            # If liked, remove the like first
            self.dislike_dao.delete_like(dislike)
        
        # Add the new dislike
        self.dislike_dao.add_dislike(dislike)
        return {"message": "Dislike added successfully"}
