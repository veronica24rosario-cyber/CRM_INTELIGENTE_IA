import os
from typing import List
from openai import OpenAI
from domain.ports import LLMPort


class OpenAIAdapter(LLMPort):
    def __init__(self, api_key: str = ""):
        api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=api_key) if api_key else None

    def ask(self, query: str, context: List[str]) -> str:
        if not self.client:
            return "Asistente no disponible: OPENAI_API_KEY no configurada"
        prompt = context[0] if context else query
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return "La API key de OpenAI no tiene créditos suficientes. El asistente funcionará en modo simulado."
            return f"Error al consultar OpenAI: {error_msg[:200]}"
