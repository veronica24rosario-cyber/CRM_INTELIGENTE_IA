from typing import List
from domain.entities import Interaction
from domain.ports import InteractionRepository


class CreateInteractionUseCase:
    def __init__(self, repo: InteractionRepository):
        self.repo = repo

    def execute(self, interaction: Interaction) -> Interaction:
        return self.repo.save(interaction)


class GetClientInteractionsUseCase:
    def __init__(self, repo: InteractionRepository):
        self.repo = repo

    def execute(self, client_id: int) -> List[Interaction]:
        return self.repo.find_by_client(client_id)
