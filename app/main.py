from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import chat, characters
from app.api.websockets import chat_ws
from app.config import settings
from app.core.session import SessionManager, get_session_manager

app = FastAPI(title="NPC Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session manager
session_manager = SessionManager()

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(characters.router, prefix="/api/characters", tags=["characters"])

# WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, session_manager: SessionManager = Depends(get_session_manager)):
    await chat_ws.chat_endpoint(websocket, session_manager)

@app.get("/")
async def root():
    return {"message": "Welcome to the NPC Backend API"}

# Dependency to get the session manager
app.dependency_overrides[get_session_manager] = lambda: session_manager

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)