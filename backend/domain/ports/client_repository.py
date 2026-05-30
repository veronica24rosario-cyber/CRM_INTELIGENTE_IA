from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Client


class ClientRepository(ABC):
    @abstractmethod
    def save(self, client: Client) -> Client:
        pass

    @abstractmethod
    def find_by_id(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    def find_all(self) -> List[Client]:
        pass

    @abstractmethod
    def search(self, query: str) -> List[Client]:
        pass

    @abstractmethod
    def delete(self, client_id: int) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
