from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Interaction


class InteractionRepository(ABC):
    @abstractmethod
    def save(self, interaction: Interaction) -> Interaction:
        pass

    @abstractmethod
    def find_by_client(self, client_id: int) -> List[Interaction]:
        pass

    @abstractmethod
    def find_all(self) -> List[Interaction]:
        pass

    @abstractmethod
    def delete(self, interaction_id: int) -> bool:
        pass
