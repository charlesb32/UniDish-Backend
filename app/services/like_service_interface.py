from abc import ABC, abstractmethod

class ILikeService(ABC):
    @abstractmethod
    def toggle_like(self, like_info):
        pass