from fastapi import WebSocket
from app.core.session import SessionManager
from app.core.llm import generate_response
from app.config import settings
from app.utils.chat_utils import format_history
import json

async def chat_endpoint(websocket: WebSocket, session_manager: SessionManager):
    await websocket.accept()
    session = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "init":
                character_id = message.get("characterId")
                language = message.get("language", settings.DEFAULT_LANGUAGE)
                session = session_manager.create_session(character_id, language)
                await websocket.send_json({"type": "init", "sessionId": session.id})
            elif message.get("type") == "chat":
                if not session:
                    await websocket.send_json({"type": "error", "message": "Session not initialized"})
                    continue

                user_message = message.get("message")
                session_manager.update_session_history(session.id, {"role": "user", "content": user_message})

                # Generate response
                history = format_history(session.history)
                response = await generate_response(user_message, session.character_id, session.language, history)

                session_manager.update_session_history(session.id, {"role": "assistant", "content": response})

                # Trim history if needed
                if settings.MAX_HISTORY_LENGTH:
                    session.history = session.history[-settings.MAX_HISTORY_LENGTH:]

                await websocket.send_json({"type": "chat", "message": response})

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if session:
            session_manager.clear_session(session.id)