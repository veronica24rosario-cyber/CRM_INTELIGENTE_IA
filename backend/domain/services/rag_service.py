from typing import List


class RAGService:
    def build_context(self, documents: List[str], max_chars: int = 3000) -> str:
        context = ""
        for doc in documents:
            if len(context) + len(doc) > max_chars:
                break
            context += doc + "\n\n"
        return context.strip()

    def format_prompt(self, query: str, context: str) -> str:
        return f"""Eres un asistente CRM experto. Usa la siguiente información del CRM para responder la pregunta del usuario.

Información del CRM:
{context}

Pregunta: {query}

Respuesta útil y concisa:"""
