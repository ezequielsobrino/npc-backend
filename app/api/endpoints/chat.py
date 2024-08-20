from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.core.session import SessionManager, get_session_manager
from app.core.llm import generate_response
from app.utils.chat_utils import format_history

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    character_id: str
    message: str
    language: str = "en"
    session_id: str = None

class ChatResponse(BaseModel):
    message: str
    session_id: str

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    session_manager: SessionManager = Depends(get_session_manager)
):
    if chat_request.session_id:
        session = session_manager.get_session(chat_request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = session_manager.create_session(chat_request.character_id, chat_request.language)

    session_manager.update_session_history(session.id, {"role": "user", "content": chat_request.message})

    history = format_history(session.history)
    response = await generate_response(chat_request.message, session.character_id, session.language, history)

    session_manager.update_session_history(session.id, {"role": "assistant", "content": response})

    # Trim history if needed
    if session_manager.max_history_length:
        session.history = session.history[-session_manager.max_history_length:]

    return ChatResponse(message=response, session_id=session.id)

@router.get("/history/{session_id}", response_model=List[ChatMessage])
async def get_chat_history(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.history