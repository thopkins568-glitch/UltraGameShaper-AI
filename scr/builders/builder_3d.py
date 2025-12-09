"""
3D builder stub: converts GameSpec dict -> 3D project JSON scaffold.
Saves output using file_saver.save_json_output and returns the project dict.
"""
from typing import Dict, Any
try:
    from src.utils.file_saver import save_json_output
except Exception:
    from ..utils.file_saver import save_json_output


def build_3d_game(game_spec: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize keys
    spec = game_spec
    if hasattr(game_spec, "dict"):
        spec = game_spec.dict()

    project = {
        "project_type": "3D",
        "title": spec.get("title", "Untitled 3D Game"),
        "engine": spec.get("engine", "unity"),
        "scene": {
            "name": "MainScene3D",
            "entities": [
                {"type": "player", "prefab": "player_3d"},
                {"type": "terrain", "prefab": "flat_terrain"}
            ],
        },
        "metadata": {
            "created_by": "builder_3d",
            "description": spec.get("description", "")
        }
    }

    save_path = save_json_output(project, prefix="game_3d")
    project["saved_to"] = save_path
    return project
