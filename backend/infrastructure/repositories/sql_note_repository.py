from typing import List
from sqlalchemy.orm import Session
from domain.entities import Note
from domain.ports import NoteRepository
from infrastructure.db.models import NoteModel


class SQLNoteRepository(NoteRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, note: Note) -> Note:
        model = NoteModel(client_id=note.client_id, content=note.content, created_by=note.created_by)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return Note(id=model.id, client_id=model.client_id, content=model.content,
                    created_by=model.created_by, created_at=model.created_at)

    def find_by_client(self, client_id: int) -> List[Note]:
        models = self.session.query(NoteModel).filter_by(client_id=client_id).all()
        return [Note(id=m.id, client_id=m.client_id, content=m.content,
                     created_by=m.created_by, created_at=m.created_at) for m in models]

    def delete(self, note_id: int) -> bool:
        model = self.session.get(NoteModel, note_id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
