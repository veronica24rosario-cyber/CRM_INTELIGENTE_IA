from abc import ABC, abstractmethod
from typing import List


class LLMPort(ABC):
    @abstractmethod
    def ask(self, query: str, context: List[str]) -> str:
        pass
