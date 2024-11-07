from abc import ABC, abstractmethod

class IDislikeService(ABC):
    @abstractmethod
    def toggle_dislike(self, dislike_info):
        pass