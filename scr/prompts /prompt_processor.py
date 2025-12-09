"""
Prompt processor:
- Defines GameSpec pydantic model
- Uses LLMClient to convert free text into validated GameSpec
- Has fallback heuristics if LLM fails
"""
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any

# Flexible import so code runs as script or package
try:
    from src.engines.llm_client import LLMClient
except Exception:
    from ..engines.llm_client import LLMClient


class GameType(str, Enum):
    TWO_D = "2D"
    THREE_D = "3D"


class GameSpec(BaseModel):
    title: str = Field(..., description="Working title")
    game_type: GameType = Field(..., description="2D or 3D")
    genre: str = Field(..., description="Game genre")
    description: str = Field(..., description="Full description")
    key_features: List[str] = Field(default_factory=list)
    engine: str = Field(..., description="unity, unreal, or godot")
    art_style: Optional[str] = None
    audio_style: Optional[str] = None


def _fallback_parse(user_input: str) -> GameSpec:
    lowered = user_input.lower()
    game_type = GameType.THREE_D if "3d" in lowered else GameType.TWO_D
    engine = "unreal" if "unreal" in lowered else ("godot" if "godot" in lowered else "unity")
    if "shooter" in lowered:
        genre = "shooter"
    elif "rpg" in lowered or "role" in lowered:
        genre = "rpg"
    elif "platform" in lowered:
        genre = "platformer"
    else:
        genre = "adventure"

    return GameSpec(
        title="Untitled Game",
        game_type=game_type,
        genre=genre,
        description=user_input.strip(),
        key_features=[],
        engine=engine,
        art_style=None,
        audio_style=None,
    )


def _build_prompt(user_input: str) -> str:
    return (
        "Convert the following game idea into a strict JSON object with these fields:\n"
        '{\n'
        '  "title": "...",\n'
        '  "game_type": "2D" or "3D",\n'
        '  "genre": "...",\n'
        '  "description": "...",\n'
        '  "key_features": ["...", "..."],\n'
        '  "engine": "unity" or "unreal" or "godot",\n'
        '  "art_style": "... or null",\n'
        '  "audio_style": "... or null"\n'
        '}\n\n'
        f"Game idea:\n{user_input}\n\nRespond ONLY with valid JSON."
    )


def generate_game_spec(user_input: str, use_llm: bool = True) -> GameSpec:
    """
    Generate a validated GameSpec. When use_llm=True, attempt LLM first, falling back
    to heuristics on any error.
    """
    if not use_llm:
        return _fallback_parse(user_input)

    llm = LLMClient()
    prompt = _build_prompt(user_input)

    try:
        raw = llm.generate_json(prompt)
        # If the LLM returns nested strings, ensure keys present
        if not isinstance(raw, dict):
            raise ValueError("LLM returned non-dict JSON")
        return GameSpec(**raw)
    except Exception:
        # Quiet fallback — we prefer to return a usable result than raise for users
        return _fallback_parse(user_input)
