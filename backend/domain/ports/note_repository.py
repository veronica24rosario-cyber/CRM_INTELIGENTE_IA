from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Note


class NoteRepository(ABC):
    @abstractmethod
    def save(self, note: Note) -> Note:
        pass

    @abstractmethod
    def find_by_client(self, client_id: int) -> List[Note]:
        pass

    @abstractmethod
    def delete(self, note_id: int) -> bool:
        pass
