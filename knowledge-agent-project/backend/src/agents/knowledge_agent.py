# backend/agents/knowledge_agent.py
from ..services.langchain_service import PDFKnowledgeBase

class KnowledgeAgent:
    def __init__(self, pdf_path: str):
        self.knowledge_base = PDFKnowledgeBase(pdf_path)

    def ask_question(self, question: str) -> str:
        return self.knowledge_base.ask_question(question)