from typing import List, Optional
from domain.entities import Client
from domain.ports import ClientRepository


class CreateClientUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, client: Client) -> Client:
        return self.repo.save(client)


class GetClientUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, client_id: int) -> Optional[Client]:
        return self.repo.find_by_id(client_id)


class ListClientsUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self) -> List[Client]:
        return self.repo.find_all()


class SearchClientsUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, query: str) -> List[Client]:
        return self.repo.search(query)


class UpdateClientUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, client: Client) -> Optional[Client]:
        existing = self.repo.find_by_id(client.id)
        if not existing:
            return None
        return self.repo.save(client)


class DeleteClientUseCase:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def execute(self, client_id: int) -> bool:
        return self.repo.delete(client_id)
