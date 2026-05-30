from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Task


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def find_by_client(self, client_id: int) -> List[Task]:
        pass

    @abstractmethod
    def find_all(self) -> List[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass
