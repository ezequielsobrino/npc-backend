# NPC Backend

This project is a backend server for managing Non-Player Characters (NPCs) in a game or interactive application. It provides APIs for character management and real-time chat functionality using historical figures as NPCs.

## Features

- Character management API with JSON-based character data
- Real-time chat with NPCs using WebSockets
- Dynamic NPC responses based on historical context and personality
- Session management for persistent conversations
- Support for multiple languages (with plans for translation)
- Integration with Groq API for natural language processing

## Technologies Used

- FastAPI
- WebSockets
- Pydantic for data validation
- CORS middleware for cross-origin requests
- Groq API for language model integration

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ezequielsobrino/npc-backend.git
   cd npc-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` or `.\venv\Scripts\Activate.ps1` in PowerShell
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your configuration:
   ```
   DEFAULT_LANGUAGE=en
   MAX_HISTORY_LENGTH=50
   GROQ_API_KEY=your_groq_api_key_here
   ```

Note: If you encounter issues activating the virtual environment on Windows, ensure you have the necessary permissions and that the PowerShell execution policy allows script execution:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

## Running the Server

To start the server, run:

```
uvicorn app.main:app --reload
```

The server will start on `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the automatic API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

To test the backend, you can use the provided HTML test page:

1. Open the file `\static\test.html` in a web browser.
2. Select a character from the dropdown menu.
3. Start chatting with the NPC using the input field and send button.

## Project Structure

```
npc-backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── chat.py
│   │   │   └── characters.py
│   │   └── websockets/
│   │       └── chat_ws.py
│   ├── core/
│   │   ├── llm.py
│   │   └── session.py
│   ├── models/
│   │   └── character.py
│   ├── utils/
│   │   └── chat_utils.py
│   ├── config.py
│   └── main.py
├── data/
│   └── characters/
│       └── *.json
├── static/
│   └── test.html
├── .env
├── requirements.txt
└── README.md
```

## Character Data

Characters are defined in JSON files located in the `data/characters/` directory. Each file contains information about a historical figure, including:

- Name
- Era
- Biography
- Achievements
- Personality traits
- Areas of knowledge
- Important relationships

## Language Model Integration

The project uses the Groq API to generate NPC responses. The `generate_response` function in `app/core/llm.py` handles the integration, creating context-aware responses based on the character's historical background and the conversation history.

## Session Management

The `SessionManager` class in `app/core/session.py` handles user sessions, maintaining conversation history and language preferences for each interaction.

## Future Enhancements

- Implement translation functionality using the Groq API
- Expand the character database
- Improve response generation with more advanced prompting techniques

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)