from pydantic import BaseModel
from typing import List, Dict
import json
from pathlib import Path

class Character(BaseModel):
    id: str
    name: str
    era: str
    bio: str
    achievements: List[str]
    personality_traits: List[str]
    knowledge_areas: List[str]
    relationships: Dict[str, str]

class CharacterManager:
    def __init__(self):
        self.characters: Dict[str, Character] = {}
        self._load_characters()

    def _load_characters(self):
        character_dir = Path(__file__).parent.parent.parent / "data" / "characters"
        print(f"Loading characters from {character_dir}")  # Debug: Path being accessed
        for file in character_dir.glob("*.json"):
            print(f"Reading file: {file}")  # Debug: File being read
            if file.stat().st_size == 0:
                print(f"Warning: {file} is empty.")  # Check if file is empty
                continue
            with file.open(encoding="utf-8") as f:
                content = f.read()
                if content:
                    data = json.loads(content)
                    character = Character(**data)
                    self.characters[character.id] = character
                else:
                    print(f"Warning: No content in {file}")  # Debug if file has no readable content

    def get_character(self, character_id: str) -> Character:
        return self.characters.get(character_id)

    def get_all_characters(self) -> List[Character]:
        return list(self.characters.values())

    def get_character_info(self, character_id: str) -> dict:
        character = self.get_character(character_id)
        if not character:
            return {}
        return {
            "name": character.name,
            "bio": character.bio,
            "era": character.era,
            "achievements": character.achievements,
            "personality_traits": character.personality_traits,
            "knowledge_areas": character.knowledge_areas,
            "relationships": character.relationships
        }

character_manager = CharacterManager()

def get_character_info(character_id: str) -> dict:
    return character_manager.get_character_info(character_id)