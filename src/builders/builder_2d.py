"""
2D builder stub: converts GameSpec dict -> 2D project JSON scaffold.
Saves output using file_saver.save_json_output and returns the project dict.
"""
from typing import Dict, Any
try:
    from src.utils.file_saver import save_json_output
except Exception:
    from ..utils.file_saver import save_json_output


def build_2d_game(game_spec: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize keys if game_spec is Pydantic model
    spec = game_spec
    if hasattr(game_spec, "dict"):
        spec = game_spec.dict()

    project = {
        "project_type": "2D",
        "title": spec.get("title", "Untitled 2D Game"),
        "engine": spec.get("engine", "unity"),
        "scene": {
            "name": "MainScene",
            "entities": [
                {"type": "player", "prefab": "player_2d"},
                {"type": "platform", "prefab": "basic_platform"},
            ],
        },
        "metadata": {
            "created_by": "builder_2d",
            "description": spec.get("description", "")
        }
    }

    save_path = save_json_output(project, prefix="game_2d")
    project["saved_to"] = save_path
    return project
