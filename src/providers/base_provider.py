from abc import ABC, abstractmethod

from src.models.schemas import ClassificationResult


class BaseProvider(ABC):
    """
    Base contract for all model providers.
    """

    @abstractmethod
    async def classify(self, query: str) -> ClassificationResult:
        """
        Classify a user query and return
        standardized classification output.
        """
        pass