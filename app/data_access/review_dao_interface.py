from abc import ABC, abstractmethod
from ..models.review import Review

class IReviewDAO(ABC):
    @abstractmethod
    def add_review(self, review: Review):
        pass