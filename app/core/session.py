from uuid import uuid4
from typing import Dict, List
from pydantic import BaseModel

class Session(BaseModel):
    id: str
    character_id: str
    language: str
    history: List[Dict[str, str]] = []

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self, character_id: str, language: str) -> Session:
        session_id = str(uuid4())
        session = Session(id=session_id, character_id=character_id, language=language)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        return self.sessions.get(session_id)

    def update_session_history(self, session_id: str, message: Dict[str, str]):
        session = self.get_session(session_id)
        if session:
            session.history.append(message)

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

def get_session_manager():
    return SessionManager()