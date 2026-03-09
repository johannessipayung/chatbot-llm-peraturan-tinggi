from fastapi import APIRouter
from pydantic import BaseModel
from app.domain.rag_service import RAGService

router = APIRouter()

rag_service = RAGService()


class QueryRequest(BaseModel):

    question: str


@router.post("/ask")

def ask_question(req: QueryRequest):

    answer = rag_service.ask(req.question)

    return {
        "response": answer
    }
