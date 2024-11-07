from abc import ABC, abstractmethod
from ..models.comment import Comment

class ICommentService(ABC):
    @abstractmethod
    def add_comment(self, comment: Comment):
        pass
    
    # @abstractmethod
    # def get_reviews(self, restaurant_id: int):
    #     pass