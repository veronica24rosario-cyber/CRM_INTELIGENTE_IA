from typing import List
from domain.entities import Note
from domain.ports import NoteRepository


class CreateNoteUseCase:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def execute(self, note: Note) -> Note:
        return self.repo.save(note)


class GetClientNotesUseCase:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def execute(self, client_id: int) -> List[Note]:
        return self.repo.find_by_client(client_id)


class DeleteNoteUseCase:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def execute(self, note_id: int) -> bool:
        return self.repo.delete(note_id)
