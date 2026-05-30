from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import User
from domain.ports import UserRepository
from infrastructure.db.models import UserModel


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        model = self.session.get(UserModel, user.id) if user.id else None
        if model:
            model.name = user.name
            model.email = user.email
            model.password_hash = user.password_hash
            model.role = user.role
        else:
            model = UserModel(name=user.name, email=user.email,
                              password_hash=user.password_hash, role=user.role)
            self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return User(id=model.id, name=model.name, email=model.email,
                    password_hash=model.password_hash, role=model.role,
                    created_at=model.created_at, updated_at=model.updated_at)

    def find_by_id(self, user_id: int) -> Optional[User]:
        model = self.session.get(UserModel, user_id)
        if not model:
            return None
        return User(id=model.id, name=model.name, email=model.email,
                    password_hash=model.password_hash, role=model.role,
                    created_at=model.created_at, updated_at=model.updated_at)

    def find_by_email(self, email: str) -> Optional[User]:
        model = self.session.query(UserModel).filter_by(email=email).first()
        if not model:
            return None
        return User(id=model.id, name=model.name, email=model.email,
                    password_hash=model.password_hash, role=model.role,
                    created_at=model.created_at, updated_at=model.updated_at)

    def find_all(self) -> List[User]:
        models = self.session.query(UserModel).all()
        return [User(id=m.id, name=m.name, email=m.email, password_hash=m.password_hash,
                     role=m.role, created_at=m.created_at, updated_at=m.updated_at) for m in models]
