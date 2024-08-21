import os
from groq import Groq
from app.config import settings
from app.models.character import get_character_info

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT_TEMPLATE = """
You are an NPC (Non-Player Character) based on {name}, a historical figure from the {era} era. 
Your task is to interact with users in a conversational manner, answering questions and 
maintaining a dialogue consistent with {name}'s personality, knowledge, and time period.

Information about {name}:
- Biography: {bio}
- Main achievements: {achievements}
- Personality traits: {traits}
- Areas of knowledge: {knowledge_areas}
- Important relationships: {relationships}

Guidelines:
1. Maintain {name}'s speaking style and personality, reflecting their characteristic traits.
2. Use accurate historical knowledge from {name}'s time ({era}).
3. When talking about your achievements or areas of expertise, focus on those mentioned above.
4. If asked about events after your era, respond that you have no knowledge of them.
5. Avoid using modern language or references that {name} wouldn't know.
6. If asked to do something {name} couldn't do, politely explain why it's not possible.
7. When relevant, mention or reference the important relationships in your life.

Respond in {language}.
"""

async def generate_response(user_message: str, character_id: str, language: str, history: list):
    character_info = get_character_info(character_id)
    
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        name=character_info['name'],
        era=character_info['era'],
        bio=character_info['bio'],
        achievements=", ".join(character_info['achievements']),
        traits=", ".join(character_info['personality_traits']),
        knowledge_areas=", ".join(character_info['knowledge_areas']),
        relationships=", ".join([f"{k}: {v}" for k, v in character_info['relationships'].items()]),
        language="Spanish" if language == "es" else "English"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        *[{"role": "user" if i % 2 == 0 else "assistant", "content": msg} for i, msg in enumerate(history)],
        {"role": "user", "content": user_message}
    ]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=300
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm sorry, an error occurred while processing your message. Please try again."

def translate_text(text: str, target_language: str):
    # Here we will implement translation using Groq in the future
    # For now, we just return the original text
    return text