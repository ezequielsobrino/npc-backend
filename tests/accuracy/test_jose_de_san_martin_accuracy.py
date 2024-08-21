import csv
import json
import asyncio
import os
from groq import Groq
from typing import List, Dict
from app.config import settings
from app.models.character import get_character_info
from app.core.llm import generate_response

# Usar la clave API de Groq desde la configuración
client = Groq(api_key=settings.GROQ_API_KEY)

async def load_questions(file_path: str) -> List[Dict[str, str]]:
    """Cargar preguntas y respuestas correctas desde un archivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

async def evaluate_response(question: str, character_response: str, correct_answer: str) -> Dict[str, float]:
    """Usar Groq para evaluar si la respuesta del personaje es correcta."""
    prompt = f"""
    Actúa como un historiador experto en José de San Martín y la independencia sudamericana. 
    Evalúa la siguiente respuesta a una pregunta sobre José de San Martín.

    Pregunta: {question}
    Respuesta del personaje: {character_response}
    Respuesta correcta: {correct_answer}

    Evalúa la respuesta del personaje en una escala de 0 a 1, donde 0 es completamente incorrecta y 1 es perfectamente correcta.
    Proporciona dos puntuaciones:
    1. Precisión: ¿Qué tan precisa es la información proporcionada en relación con los hechos históricos conocidos?
    2. Relevancia: ¿Qué tan relevante es la respuesta a la pregunta específica sobre José de San Martín?

    Responde solo con un objeto JSON que contenga estas dos puntuaciones, sin explicación adicional.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=100
        )
        evaluation = json.loads(chat_completion.choices[0].message.content)
        return evaluation
    except Exception as e:
        print(f"Error al evaluar respuesta: {str(e)}")
        return {"precision": 0, "relevancia": 0}

async def run_accuracy_test(questions_file: str, character_id: str, output_file: str):
    questions = await load_questions(questions_file)
    results = []
    total_precision = 0
    total_relevancia = 0
    
    for i, qa_pair in enumerate(questions, 1):
        question = qa_pair['question']
        correct_answer = qa_pair['answer']
        
        # Usar la función generate_response directamente
        character_response = await generate_response(question, character_id, settings.DEFAULT_LANGUAGE, [])
        evaluation = await evaluate_response(question, character_response, correct_answer)
        
        total_precision += evaluation['precision']
        total_relevancia += evaluation['relevancia']
        
        results.append({
            'question_id': i,
            'question': question,
            'correct_answer': correct_answer,
            'character_response': character_response,
            'precision': evaluation['precision'],
            'relevancia': evaluation['relevancia']
        })
        
        print(f"Procesada pregunta {i}/{len(questions)}")
    
    avg_precision = total_precision / len(questions)
    avg_relevancia = total_relevancia / len(questions)
    
    # Crear el directorio para el archivo de salida si no existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Guardar resultados en CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['question_id', 'question', 'correct_answer', 'character_response', 'precision', 'relevancia'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Resultados guardados en {output_file}")
    print(f"Precisión promedio: {avg_precision:.2f}")
    print(f"Relevancia promedio: {avg_relevancia:.2f}")

if __name__ == "__main__":
    # Ajusta estas rutas según la estructura de tu proyecto
    questions_file = "tests/data/jose_de_san_martin_questions.json"
    character_id = "jose_de_san_martin"
    output_file = "tests/results/accuracy_results_jose_de_san_martin.csv"
    
    asyncio.run(run_accuracy_test(questions_file, character_id, output_file))