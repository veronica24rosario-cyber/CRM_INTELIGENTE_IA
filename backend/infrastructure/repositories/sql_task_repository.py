from typing import Optional, List
from sqlalchemy.orm import Session
from domain.entities import Task
from domain.ports import TaskRepository
from infrastructure.db.models import TaskModel


class SQLTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task) -> Task:
        model = self.session.get(TaskModel, task.id) if task.id else None
        if model:
            model.title = task.title
            model.description = task.description
            model.status = task.status
            model.priority = task.priority
            model.due_date = task.due_date
            model.client_id = task.client_id
            model.assigned_to = task.assigned_to
        else:
            model = TaskModel(title=task.title, description=task.description,
                              status=task.status, priority=task.priority,
                              due_date=task.due_date, client_id=task.client_id,
                              assigned_to=task.assigned_to)
            self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return Task(id=model.id, client_id=model.client_id, title=model.title,
                    description=model.description, status=model.status,
                    priority=model.priority, due_date=model.due_date,
                    assigned_to=model.assigned_to, created_at=model.created_at)

    def find_by_id(self, task_id: int) -> Optional[Task]:
        model = self.session.get(TaskModel, task_id)
        if not model:
            return None
        return Task(id=model.id, client_id=model.client_id, title=model.title,
                    description=model.description, status=model.status,
                    priority=model.priority, due_date=model.due_date,
                    assigned_to=model.assigned_to, created_at=model.created_at)

    def find_by_client(self, client_id: int) -> List[Task]:
        models = self.session.query(TaskModel).filter_by(client_id=client_id).all()
        return [Task(id=m.id, client_id=m.client_id, title=m.title, description=m.description,
                     status=m.status, priority=m.priority, due_date=m.due_date,
                     assigned_to=m.assigned_to, created_at=m.created_at) for m in models]

    def find_all(self) -> List[Task]:
        models = self.session.query(TaskModel).all()
        return [Task(id=m.id, client_id=m.client_id, title=m.title, description=m.description,
                     status=m.status, priority=m.priority, due_date=m.due_date,
                     assigned_to=m.assigned_to, created_at=m.created_at) for m in models]

    def delete(self, task_id: int) -> bool:
        model = self.session.get(TaskModel, task_id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
