from abc import ABC, abstractmethod
from ..models.comment import Comment

class ICommentDAO(ABC):
    @abstractmethod
    def add_comment(self, comment: Comment):
        pass
    
    # @abstractmethod
    # def get_comments(self, user_id, review_id: int):
    #     pass