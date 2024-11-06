from abc import ABC, abstractmethod
from ..models.review import Review

class IReviewService(ABC):
    @abstractmethod
    def add_review(self, review: Review):
        pass