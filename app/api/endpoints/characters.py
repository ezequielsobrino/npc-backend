from fastapi import APIRouter, HTTPException
from app.models.character import character_manager, Character
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Character])
async def get_all_characters():
    """
    Retrieve a list of all available characters.
    """
    return character_manager.get_all_characters()

@router.get("/{character_id}", response_model=dict)
async def get_character(character_id: str):
    """
    Retrieve detailed information about a specific character.
    """
    character_info = character_manager.get_character_info(character_id)
    if not character_info:
        raise HTTPException(status_code=404, detail=f"Character with id {character_id} not found")
    return character_info

@router.get("/{character_id}/summary", response_model=dict)
async def get_character_summary(character_id: str):
    """
    Retrieve a summary of a character, including only basic information.
    """
    character = character_manager.get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail=f"Character with id {character_id} not found")
    return {
        "id": character.id,
        "name": character.name,
        "era": character.era,
        "short_bio": character.bio[:100] + "..." if len(character.bio) > 100 else character.bio
    }

@router.get("/{character_id}/achievements", response_model=List[str])
async def get_character_achievements(character_id: str):
    """
    Retrieve the list of achievements for a specific character.
    """
    character = character_manager.get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail=f"Character with id {character_id} not found")
    return character.achievements