from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import Interaction
from domain.ports import InteractionRepository
from infrastructure.db.models import InteractionModel


class SQLInteractionRepository(InteractionRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, interaction: Interaction) -> Interaction:
        model = InteractionModel(
            client_id=interaction.client_id, user_id=interaction.user_id,
            type=interaction.type, subject=interaction.subject,
            description=interaction.description,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return Interaction(id=model.id, client_id=model.client_id, user_id=model.user_id,
                           type=model.type, subject=model.subject, description=model.description,
                           created_at=model.created_at)

    def find_by_client(self, client_id: int) -> List[Interaction]:
        models = self.session.query(InteractionModel).filter_by(client_id=client_id).all()
        return [Interaction(id=m.id, client_id=m.client_id, user_id=m.user_id,
                            type=m.type, subject=m.subject, description=m.description,
                            created_at=m.created_at) for m in models]

    def find_all(self) -> List[Interaction]:
        models = self.session.query(InteractionModel).all()
        return [Interaction(id=m.id, client_id=m.client_id, user_id=m.user_id,
                            type=m.type, subject=m.subject, description=m.description,
                            created_at=m.created_at) for m in models]

    def delete(self, interaction_id: int) -> bool:
        model = self.session.get(InteractionModel, interaction_id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
