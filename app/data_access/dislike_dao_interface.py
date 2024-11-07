from abc import ABC, abstractmethod
from ..models.dislike import Dislike

class IDislikeDAO(ABC):
    @abstractmethod
    def has_existing_dislike(self, dislike: Dislike):
        pass
    
    @abstractmethod
    def add_dislike(self, dislike: Dislike):
        pass
    
    @abstractmethod
    def delete_dislike(self, dislike: Dislike):
        pass

    @abstractmethod
    def has_existing_like(self, dislike: Dislike):
        pass

    @abstractmethod
    def delete_like(self, dislike: Dislike):
        pass