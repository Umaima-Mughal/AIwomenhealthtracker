from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.db_models.chat import ChatMessage
from modules.medical_chatbot import generate_response


router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=data.message,
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    answer = generate_response(data.message)

    assistant_message = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=answer,
    )

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": answer}


@router.get("/")
def get_chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )