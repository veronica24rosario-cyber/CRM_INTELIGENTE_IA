from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import Client
from domain.ports import ClientRepository
from infrastructure.db.models import ClientModel


class SQLClientRepository(ClientRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, client: Client) -> Client:
        model = self.session.get(ClientModel, client.id) if client.id else None
        if model:
            model.name = client.name
            model.email = client.email
            model.phone = client.phone
            model.company = client.company
            model.notes = client.notes
            model.owner_id = client.owner_id
        else:
            model = ClientModel(
                name=client.name, email=client.email, phone=client.phone,
                company=client.company, notes=client.notes, owner_id=client.owner_id,
            )
            self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return Client(id=model.id, name=model.name, email=model.email,
                      phone=model.phone, company=model.company, notes=model.notes or "",
                      owner_id=model.owner_id, created_at=model.created_at, updated_at=model.updated_at)

    def find_by_id(self, client_id: int) -> Optional[Client]:
        model = self.session.get(ClientModel, client_id)
        if not model:
            return None
        return Client(id=model.id, name=model.name, email=model.email,
                      phone=model.phone, company=model.company, notes=model.notes or "",
                      owner_id=model.owner_id, created_at=model.created_at, updated_at=model.updated_at)

    def find_all(self) -> List[Client]:
        models = self.session.query(ClientModel).all()
        return [Client(id=m.id, name=m.name, email=m.email, phone=m.phone,
                       company=m.company, notes=m.notes or "", owner_id=m.owner_id,
                       created_at=m.created_at, updated_at=m.updated_at) for m in models]

    def search(self, query: str) -> List[Client]:
        like = f"%{query}%"
        models = self.session.query(ClientModel).filter(
            ClientModel.name.ilike(like) | ClientModel.email.ilike(like) |
            ClientModel.company.ilike(like) | ClientModel.notes.ilike(like)
        ).all()
        return [Client(id=m.id, name=m.name, email=m.email, phone=m.phone,
                       company=m.company, notes=m.notes or "", owner_id=m.owner_id,
                       created_at=m.created_at, updated_at=m.updated_at) for m in models]

    def delete(self, client_id: int) -> bool:
        model = self.session.get(ClientModel, client_id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True

    def count(self) -> int:
        return self.session.query(ClientModel).count()
