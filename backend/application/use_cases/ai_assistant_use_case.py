import re
from typing import List
from domain.ports import ClientRepository, InteractionRepository, DealRepository, NoteRepository, TaskRepository, LLMPort
from domain.services.rag_service import RAGService


class AIAssistantUseCase:
    def __init__(
        self,
        client_repo: ClientRepository,
        interaction_repo: InteractionRepository,
        deal_repo: DealRepository,
        note_repo: NoteRepository,
        task_repo: TaskRepository,
        llm: LLMPort,
    ):
        self.client_repo = client_repo
        self.interaction_repo = interaction_repo
        self.deal_repo = deal_repo
        self.note_repo = note_repo
        self.task_repo = task_repo
        self.llm = llm
        self.rag = RAGService()

    def _detect_intent(self, query: str) -> str:
        q = query.lower()
        if re.search(r"cliente|clientes|contacto|empresa", q):
            return "clients"
        if re.search(r"oportunidad|oportunidades|trato|tratos|deal|pipeline|venta", q):
            return "deals"
        if re.search(r"tarea|tareas|pendiente|pendientes|hacer|to.do", q):
            return "tasks"
        if re.search(r"resumen|general|panorama|dashboard|como vamos|todo", q):
            return "summary"
        return "general"

    def ask(self, query: str) -> str:
        intent = self._detect_intent(query)
        docs: List[str] = []

        if intent == "clients":
            clients = self.client_repo.search(query)
            if not clients:
                clients = self.client_repo.find_all()
            for c in clients:
                docs.append(f"Cliente: {c.name}, Email: {c.email}, Empresa: {c.company}, Telefono: {c.phone}, Notas: {c.notes}")
                for d in self.deal_repo.find_by_client(c.id):
                    docs.append(f"  Oportunidad: {d.title} - ${d.value} - Etapa: {d.stage}")

        elif intent == "deals":
            all_deals = self.deal_repo.find_all()
            for d in all_deals:
                client_name = ""
                try:
                    client = self.client_repo.find_by_id(d.client_id)
                    if client:
                        client_name = client.name
                except:
                    pass
                docs.append(f"Oportunidad: {d.title}, Cliente: {client_name}, Valor: ${d.value}, Etapa: {d.stage}")

        elif intent == "tasks":
            all_tasks = self.task_repo.find_all()
            for t in all_tasks:
                client_name = ""
                try:
                    client = self.client_repo.find_by_id(t.client_id)
                    if client:
                        client_name = client.name
                except:
                    pass
                docs.append(f"Tarea: {t.title}, Cliente: {client_name}, Prioridad: {t.priority}, Estado: {t.status}, Vencimiento: {t.due_date}")

        else:
            # summary or general - traer conteos
            clients = self.client_repo.find_all()
            all_deals = self.deal_repo.find_all()
            all_tasks = self.task_repo.find_all()
            docs.append(f"Total clientes: {len(clients)}")
            docs.append(f"Total oportunidades: {len(all_deals)}")
            docs.append(f"Total tareas: {len(all_tasks)}")
            for c in clients[:5]:
                docs.append(f"Cliente: {c.name}, Email: {c.email}, Empresa: {c.company}")
            stage_counts = {}
            for d in all_deals:
                stage_counts[d.stage] = stage_counts.get(d.stage, 0) + 1
            for stage, count in stage_counts.items():
                docs.append(f"  Oportunidades en {stage}: {count}")

        context = self.rag.build_context(docs)
        prompt = self.rag.format_prompt(query, context)
        return self.llm.ask(query, [prompt])
