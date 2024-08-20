from app.config import settings

def format_history(history):
    if settings.HISTORY_FORMAT == "simple":
        return [f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in history]
    elif settings.HISTORY_FORMAT == "detailed":
        return [{"role": msg["role"], "content": msg["content"]} for msg in history]
    else:
        return history