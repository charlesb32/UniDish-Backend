from abc import ABC, abstractmethod
from ..models.like import Like

class ILikeDAO(ABC):
    @abstractmethod
    def has_existing_like(self, like: Like):
        pass

    @abstractmethod
    def add_like(self, like: Like):
        pass

    @abstractmethod
    def delete_like(self, like: Like):
        pass

    @abstractmethod
    def has_existing_dislike(self, like: Like):
        pass

    @abstractmethod
    def delete_dislike(self, like: Like):
        pass
