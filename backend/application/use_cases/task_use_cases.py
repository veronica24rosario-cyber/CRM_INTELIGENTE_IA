from typing import List, Optional
from domain.entities import Task
from domain.ports import TaskRepository


class CreateTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task: Task) -> Task:
        return self.repo.save(task)


class GetTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task_id: int) -> Optional[Task]:
        return self.repo.find_by_id(task_id)


class ListTasksUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self) -> List[Task]:
        return self.repo.find_all()


class UpdateTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task: Task) -> Optional[Task]:
        existing = self.repo.find_by_id(task.id)
        if not existing:
            return None
        return self.repo.save(task)


class DeleteTaskUseCase:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def execute(self, task_id: int) -> bool:
        return self.repo.delete(task_id)
