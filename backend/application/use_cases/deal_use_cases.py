from typing import List, Optional
from domain.entities import Deal
from domain.ports import DealRepository


class CreateDealUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self, deal: Deal) -> Deal:
        return self.repo.save(deal)


class GetDealUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self, deal_id: int) -> Optional[Deal]:
        return self.repo.find_by_id(deal_id)


class ListDealsUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self) -> List[Deal]:
        return self.repo.find_all()


class GetClientDealsUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self, client_id: int) -> List[Deal]:
        return self.repo.find_by_client(client_id)


class UpdateDealUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self, deal: Deal) -> Optional[Deal]:
        existing = self.repo.find_by_id(deal.id)
        if not existing:
            return None
        return self.repo.save(deal)


class DeleteDealUseCase:
    def __init__(self, repo: DealRepository):
        self.repo = repo

    def execute(self, deal_id: int) -> bool:
        return self.repo.delete(deal_id)
