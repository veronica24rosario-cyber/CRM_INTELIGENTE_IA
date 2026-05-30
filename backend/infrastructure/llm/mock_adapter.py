import re
from typing import List
from domain.ports import LLMPort


class MockLLMAdapter(LLMPort):
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

    def ask(self, query: str, context: List[str]) -> str:
        prompt = context[0] if context else ""
        intent = self._detect_intent(query)

        info_part = ""
        if "Informaci\u00f3n del CRM:" in prompt:
            info_part = prompt.split("Informaci\u00f3n del CRM:")[1]
            if "Pregunta:" in info_part:
                info_part = info_part.split("Pregunta:")[0].strip()

        if not info_part or not info_part.strip():
            return self._no_data_response(query, intent)

        lines = [l.strip() for l in info_part.split("\n") if l.strip()]

        if intent == "clients":
            return self._format_clients(lines)
        elif intent == "deals":
            return self._format_deals(lines)
        elif intent == "tasks":
            return self._format_tasks(lines)
        else:
            return self._format_summary(lines, query)

    def _no_data_response(self, query: str, intent: str) -> str:
        if intent == "clients":
            return "No encontr\u00e9 clientes registrados en el CRM. Puedes agregar clientes desde la secci\u00f3n de Clientes."
        if intent == "deals":
            return "No encontr\u00e9 oportunidades registradas. Puedes crear oportunidades desde la secci\u00f3n de Oportunidades."
        if intent == "tasks":
            return "No encontr\u00e9 tareas pendientes. Puedes crear tareas desde la secci\u00f3n de Tareas."
        return (
            "Hola, soy el asistente del CRM Inteligente.\n\n"
            "Puedes preguntarme sobre:\n"
            "- Clientes: informaci\u00f3n y estado de tus clientes\n"
            "- Oportunidades: seguimiento de negocios\n"
            "- Tareas: pendientes y prioridades\n\n"
            "\u00bfQu\u00e9 deseas consultar?"
        )

    def _format_clients(self, lines: List[str]) -> str:
        client_lines = [l for l in lines if l.startswith("Cliente:")]
        if not client_lines:
            return "No encontr\u00e9 clientes registrados en el CRM."

        resp = f"Tienes **{len(client_lines)} clientes** registrados:\n\n"
        for cl in client_lines:
            cl = cl.replace("Cliente:", "").strip()
            parts = [p.strip() for p in cl.split(",")]
            name = parts[0] if parts else ""
            email = ""
            company = ""
            phone = ""
            for p in parts[1:]:
                if p.lower().startswith("email:"):
                    email = p.split(":", 1)[1].strip()
                elif p.lower().startswith("empresa:"):
                    company = p.split(":", 1)[1].strip()
                elif p.lower().startswith("telefono:"):
                    phone = p.split(":", 1)[1].strip()
            resp += f"  \u2022 {name}"
            if company:
                resp += f" ({company})"
            if email:
                resp += f" - {email}"
            if phone:
                resp += f" - Tel: {phone}"
            resp += "\n"

        # Add deals that belong to these clients
        deal_lines = [l for l in lines if l.startswith("Oportunidad:")]
        if deal_lines:
            resp += f"\nOportunidades asociadas:\n"
            for dl in deal_lines:
                dl = dl.replace("Oportunidad:", "").strip()
                resp += f"  \u2022 {dl}\n"

        return resp

    def _format_deals(self, lines: List[str]) -> str:
        deal_lines = [l for l in lines if l.startswith("Oportunidad:")]
        if not deal_lines:
            return "No encontr\u00e9 oportunidades registradas en el CRM."

        # contar por etapa
        stages = {}
        for dl in deal_lines:
            dl_clean = dl.replace("Oportunidad:", "").strip()
            if "Etapa:" in dl_clean:
                stage = dl_clean.split("Etapa:")[1].strip()
                stages[stage] = stages.get(stage, 0) + 1

        resp = f"Tienes **{len(deal_lines)} oportunidades** en total:\n\n"
        if stages:
            resp += "Distribuci\u00f3n por etapa:\n"
            for stage, count in stages.items():
                resp += f"  \u2022 {stage}: {count}\n"
            resp += "\n"

        resp += "Detalle:\n"
        for dl in deal_lines:
            dl_clean = dl.replace("Oportunidad:", "").strip()
            resp += f"  \u2022 {dl_clean}\n"
        return resp

    def _format_tasks(self, lines: List[str]) -> str:
        task_lines = [l for l in lines if l.startswith("Tarea:")]
        if not task_lines:
            return "No encontr\u00e9 tareas registradas en el CRM."

        pendientes = [l for l in task_lines if "Estado: pending" in l or "Estado: Pending" in l or "Estado: pendiente" in l]
        completadas = [l for l in task_lines if "Estado: completed" in l or "Estado: Completed" in l]

        resp = f"Tienes **{len(task_lines)} tareas** registradas"
        if pendientes:
            resp += f" ({len(pendientes)} pendientes)"
        if completadas:
            resp += f" ({len(completadas)} completadas)"
        resp += ":\n\n"

        for tl in task_lines:
            tl_clean = tl.replace("Tarea:", "").strip()
            resp += f"  \u2022 {tl_clean}\n"
        return resp

    def _format_summary(self, lines: List[str], query: str) -> str:
        # buscar totales
        total_clients = 0
        total_deals = 0
        total_tasks = 0
        for l in lines:
            if l.startswith("Total clientes:"):
                try: total_clients = int(l.split(":")[1].strip())
                except: pass
            if l.startswith("Total oportunidades:"):
                try: total_deals = int(l.split(":")[1].strip())
                except: pass
            if l.startswith("Total tareas:"):
                try: total_tasks = int(l.split(":")[1].strip())
                except: pass

        q = query.lower()
        if "total" in q or "cuantos" in q or "cuantas" in q or "cu\u00e1ntos" in q or "cu\u00e1ntas" in q:
            resp = "Resumen del CRM:\n\n"
            resp += f"  \u2022 Clientes: {total_clients}\n"
            resp += f"  \u2022 Oportunidades: {total_deals}\n"
            resp += f"  \u2022 Tareas: {total_tasks}\n"
            return resp

        # mostrar resumen completo
        resp = f"**Resumen del CRM**\n\n"
        resp += f"  \u2022 Clientes: {total_clients}\n"
        resp += f"  \u2022 Oportunidades: {total_deals}\n"
        resp += f"  \u2022 Tareas: {total_tasks}\n\n"

        client_lines = [l for l in lines if l.startswith("Cliente:")]
        if client_lines:
            resp += f"**Clientes ({len(client_lines)}):**\n"
            for cl in client_lines[:5]:
                cl = cl.replace("Cliente:", "").strip()
                parts = [p.strip() for p in cl.split(",")]
                name = parts[0] if parts else ""
                company = ""
                for p in parts[1:]:
                    if p.lower().startswith("empresa:"):
                        company = p.split(":", 1)[1].strip()
                resp += f"  \u2022 {name}"
                if company:
                    resp += f" ({company})"
                resp += "\n"

        deal_stage_lines = [l for l in lines if l.startswith("Oportunidades en")]
        if deal_stage_lines:
            resp += f"\n**Oportunidades por etapa:**\n"
            for sl in deal_stage_lines:
                resp += f"  \u2022 {sl}\n"

        return resp
