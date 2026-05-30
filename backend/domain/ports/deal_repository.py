from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Deal


class DealRepository(ABC):
    @abstractmethod
    def save(self, deal: Deal) -> Deal:
        pass

    @abstractmethod
    def find_by_id(self, deal_id: int) -> Optional[Deal]:
        pass

    @abstractmethod
    def find_by_client(self, client_id: int) -> List[Deal]:
        pass

    @abstractmethod
    def find_all(self) -> List[Deal]:
        pass

    @abstractmethod
    def delete(self, deal_id: int) -> bool:
        pass
