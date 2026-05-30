from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from infrastructure.db.database import get_db
from infrastructure.repositories.sql_client_repository import SQLClientRepository
from infrastructure.repositories.sql_interaction_repository import SQLInteractionRepository
from infrastructure.repositories.sql_deal_repository import SQLDealRepository
from infrastructure.repositories.sql_task_repository import SQLTaskRepository
from infrastructure.repositories.sql_note_repository import SQLNoteRepository
from application.use_cases.client_use_cases import *
from application.use_cases.interaction_use_cases import *
from application.use_cases.deal_use_cases import *
from application.use_cases.task_use_cases import *
from application.use_cases.note_use_cases import *

router = APIRouter(prefix="/api")


class ClientIn(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    company: str = ""
    notes: str = ""


class ClientOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    company: str
    notes: str
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class InteractionIn(BaseModel):
    client_id: int
    type: str = "call"
    subject: str = ""
    description: str = ""


class InteractionOut(BaseModel):
    id: int
    client_id: int
    type: str
    subject: str
    description: str
    created_at: datetime


class DealIn(BaseModel):
    client_id: int
    title: str = ""
    value: float = 0.0
    stage: str = "lead"


class DealOut(BaseModel):
    id: int
    client_id: int
    title: str
    value: float
    stage: str
    created_at: datetime
    updated_at: datetime


class TaskIn(BaseModel):
    client_id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: str = "pending"
    priority: str = "medium"


class TaskOut(BaseModel):
    id: int
    client_id: Optional[int] = None
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime


class NoteIn(BaseModel):
    client_id: int
    content: str = ""


class NoteOut(BaseModel):
    id: int
    client_id: int
    content: str
    created_at: datetime


class AskIn(BaseModel):
    query: str


class AskOut(BaseModel):
    response: str


class StatsOut(BaseModel):
    total_clients: int
    total_deals: int
    total_tasks: int
    total_interactions: int


def get_client_repo(db: Session = Depends(get_db)):
    return SQLClientRepository(db)


def get_interaction_repo(db: Session = Depends(get_db)):
    return SQLInteractionRepository(db)


def get_deal_repo(db: Session = Depends(get_db)):
    return SQLDealRepository(db)


def get_task_repo(db: Session = Depends(get_db)):
    return SQLTaskRepository(db)


def get_note_repo(db: Session = Depends(get_db)):
    return SQLNoteRepository(db)


@router.post("/clients", response_model=ClientOut)
def create_client(data: ClientIn, repo=Depends(get_client_repo)):
    from domain.entities import Client
    uc = CreateClientUseCase(repo)
    client = Client(name=data.name, email=data.email, phone=data.phone,
                    company=data.company, notes=data.notes)
    return uc.execute(client)


@router.get("/clients", response_model=List[ClientOut])
def list_clients(search: str = "", repo=Depends(get_client_repo)):
    if search:
        uc = SearchClientsUseCase(repo)
        return uc.execute(search)
    uc = ListClientsUseCase(repo)
    return uc.execute()


@router.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: int, repo=Depends(get_client_repo)):
    uc = GetClientUseCase(repo)
    client = uc.execute(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


@router.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, data: ClientIn, repo=Depends(get_client_repo)):
    from domain.entities import Client
    uc = UpdateClientUseCase(repo)
    client = Client(id=client_id, name=data.name, email=data.email,
                    phone=data.phone, company=data.company, notes=data.notes)
    result = uc.execute(client)
    if not result:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return result


@router.delete("/clients/{client_id}")
def delete_client(client_id: int, repo=Depends(get_client_repo)):
    uc = DeleteClientUseCase(repo)
    if not uc.execute(client_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"ok": True}


@router.post("/interactions", response_model=InteractionOut)
def create_interaction(data: InteractionIn, repo=Depends(get_interaction_repo)):
    from domain.entities import Interaction
    uc = CreateInteractionUseCase(repo)
    interaction = Interaction(client_id=data.client_id, type=data.type,
                              subject=data.subject, description=data.description)
    return uc.execute(interaction)


@router.get("/clients/{client_id}/interactions", response_model=List[InteractionOut])
def get_client_interactions(client_id: int, repo=Depends(get_interaction_repo)):
    uc = GetClientInteractionsUseCase(repo)
    return uc.execute(client_id)


@router.post("/deals", response_model=DealOut)
def create_deal(data: DealIn, repo=Depends(get_deal_repo)):
    from domain.entities import Deal
    uc = CreateDealUseCase(repo)
    deal = Deal(client_id=data.client_id, title=data.title,
                value=data.value, stage=data.stage)
    return uc.execute(deal)


@router.get("/deals", response_model=List[DealOut])
def list_deals(repo=Depends(get_deal_repo)):
    uc = ListDealsUseCase(repo)
    return uc.execute()


@router.get("/deals/{deal_id}", response_model=DealOut)
def get_deal(deal_id: int, repo=Depends(get_deal_repo)):
    uc = GetDealUseCase(repo)
    deal = uc.execute(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    return deal


@router.put("/deals/{deal_id}", response_model=DealOut)
def update_deal(deal_id: int, data: DealIn, repo=Depends(get_deal_repo)):
    from domain.entities import Deal
    uc = UpdateDealUseCase(repo)
    deal = Deal(id=deal_id, client_id=data.client_id, title=data.title,
                value=data.value, stage=data.stage)
    result = uc.execute(deal)
    if not result:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    return result


@router.delete("/deals/{deal_id}")
def delete_deal(deal_id: int, repo=Depends(get_deal_repo)):
    uc = DeleteDealUseCase(repo)
    if not uc.execute(deal_id):
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")
    return {"ok": True}


@router.post("/tasks", response_model=TaskOut)
def create_task(data: TaskIn, repo=Depends(get_task_repo)):
    from domain.entities import Task
    uc = CreateTaskUseCase(repo)
    task = Task(client_id=data.client_id, title=data.title,
                description=data.description, status=data.status, priority=data.priority)
    return uc.execute(task)


@router.get("/tasks", response_model=List[TaskOut])
def list_tasks(repo=Depends(get_task_repo)):
    uc = ListTasksUseCase(repo)
    return uc.execute()


@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, repo=Depends(get_task_repo)):
    uc = GetTaskUseCase(repo)
    task = uc.execute(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskIn, repo=Depends(get_task_repo)):
    from domain.entities import Task
    uc = UpdateTaskUseCase(repo)
    task = Task(id=task_id, client_id=data.client_id, title=data.title,
                description=data.description, status=data.status, priority=data.priority)
    result = uc.execute(task)
    if not result:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return result


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, repo=Depends(get_task_repo)):
    uc = DeleteTaskUseCase(repo)
    if not uc.execute(task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"ok": True}


@router.post("/notes", response_model=NoteOut)
def create_note(data: NoteIn, repo=Depends(get_note_repo)):
    from domain.entities import Note
    uc = CreateNoteUseCase(repo)
    note = Note(client_id=data.client_id, content=data.content)
    return uc.execute(note)


@router.get("/clients/{client_id}/notes", response_model=List[NoteOut])
def get_client_notes(client_id: int, repo=Depends(get_note_repo)):
    uc = GetClientNotesUseCase(repo)
    return uc.execute(client_id)


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, repo=Depends(get_note_repo)):
    uc = DeleteNoteUseCase(repo)
    if not uc.execute(note_id):
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return {"ok": True}


@router.post("/assistant/ask", response_model=AskOut)
def assistant_ask(data: AskIn, cr=Depends(get_client_repo),
                  ir=Depends(get_interaction_repo), dr=Depends(get_deal_repo),
                  nr=Depends(get_note_repo), tr=Depends(get_task_repo)):
    from application.use_cases.ai_assistant_use_case import AIAssistantUseCase
    from infrastructure.llm.mock_adapter import MockLLMAdapter
    use_case = AIAssistantUseCase(client_repo=cr, interaction_repo=ir,
                                  deal_repo=dr, note_repo=nr, task_repo=tr,
                                  llm=MockLLMAdapter())
    response = use_case.ask(data.query)
    return AskOut(response=response)


@router.get("/stats", response_model=StatsOut)
def get_stats(cr=Depends(get_client_repo), dr=Depends(get_deal_repo),
              tr=Depends(get_task_repo), ir=Depends(get_interaction_repo)):
    return StatsOut(
        total_clients=cr.count(),
        total_deals=len(dr.find_all()),
        total_tasks=len(tr.find_all()),
        total_interactions=len(ir.find_all()),
    )
