from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import Deal
from domain.ports import DealRepository
from infrastructure.db.models import DealModel


class SQLDealRepository(DealRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, deal: Deal) -> Deal:
        model = self.session.get(DealModel, deal.id) if deal.id else None
        if model:
            model.title = deal.title
            model.value = deal.value
            model.stage = deal.stage
            model.client_id = deal.client_id
            model.owner_id = deal.owner_id
        else:
            model = DealModel(client_id=deal.client_id, title=deal.title, value=deal.value,
                              stage=deal.stage, owner_id=deal.owner_id)
            self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return Deal(id=model.id, client_id=model.client_id, title=model.title,
                    value=model.value, stage=model.stage, owner_id=model.owner_id,
                    created_at=model.created_at, updated_at=model.updated_at)

    def find_by_id(self, deal_id: int) -> Optional[Deal]:
        model = self.session.get(DealModel, deal_id)
        if not model:
            return None
        return Deal(id=model.id, client_id=model.client_id, title=model.title,
                    value=model.value, stage=model.stage, owner_id=model.owner_id,
                    created_at=model.created_at, updated_at=model.updated_at)

    def find_by_client(self, client_id: int) -> List[Deal]:
        models = self.session.query(DealModel).filter_by(client_id=client_id).all()
        return [Deal(id=m.id, client_id=m.client_id, title=m.title, value=m.value,
                     stage=m.stage, owner_id=m.owner_id, created_at=m.created_at,
                     updated_at=m.updated_at) for m in models]

    def find_all(self) -> List[Deal]:
        models = self.session.query(DealModel).all()
        return [Deal(id=m.id, client_id=m.client_id, title=m.title, value=m.value,
                     stage=m.stage, owner_id=m.owner_id, created_at=m.created_at,
                     updated_at=m.updated_at) for m in models]

    def delete(self, deal_id: int) -> bool:
        model = self.session.get(DealModel, deal_id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
