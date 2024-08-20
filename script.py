import os

# Base directory path
base_dir = r'D:\repos\npc-backend'

# Directory structure
dirs = [
    "app",
    "app/api",
    "app/api/endpoints",
    "app/api/websockets",
    "app/core",
    "app/models",
    "app/utils",
    "tests",
    "tests/test_api",
    "tests/test_core",
    "data",
    "data/characters",
    "data/languages"
]

# Files to be created in the directory structure
files = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/api/__init__.py",
    "app/api/endpoints/__init__.py",
    "app/api/endpoints/chat.py",
    "app/api/endpoints/characters.py",
    "app/api/websockets/__init__.py",
    "app/api/websockets/chat_ws.py",
    "app/core/__init__.py",
    "app/core/llm.py",
    "app/core/character.py",
    "app/core/language.py",
    "app/models/__init__.py",
    "app/models/character.py",
    "app/models/language.py",
    "app/utils/__init__.py",
    "app/utils/helpers.py",
    "tests/__init__.py",
    "tests/test_api/__init__.py",
    "tests/test_api/test_chat.py",
    "tests/test_api/test_characters.py",
    "tests/test_core/__init__.py",
    "tests/test_core/test_llm.py",
    "tests/test_core/test_character.py",
    "tests/test_core/test_language.py",
    "data/characters/leonardo_da_vinci.json",
    "data/characters/jose_de_san_martin.json",
    "data/languages/en.json",
    "data/languages/es.json",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "README.md",
    "Dockerfile"
]

def create_directories(base, dirs):
    for dir in dirs:
        dir_path = os.path.join(base, dir)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory created: {dir_path}")

def create_files(base, files):
    for file in files:
        file_path = os.path.join(base, file)
        with open(file_path, 'w') as f:
            pass  # Create empty file
        print(f"File created: {file_path}")

if __name__ == "__main__":
    create_directories(base_dir, dirs)
    create_files(base_dir, files)
