#!/usr/bin/env python3
"""
CLI runner for GameShaper-AI.
Usage:
  python src/main.py --idea "A 2D puzzler about light and shadow"
  python src/main.py --idea "A 3D mech shooter" --no-llm
"""
import argparse
import json
import sys

# Import flexible style so script works whether executed from repo root or installed
try:
    from src.prompts.prompt_processor import generate_game_spec
    from src.builders.builder_2d import build_2d_game
    from src.builders.builder_3d import build_3d_game
except Exception:
    from prompts.prompt_processor import generate_game_spec
    from builders.builder_2d import build_2d_game
    from builders.builder_3d import build_3d_game


def run(idea: str, use_llm: bool = True):
    spec = generate_game_spec(idea, use_llm=use_llm)
    # spec is a Pydantic model; convert to dict
    try:
        spec_dict = json.loads(spec.json())
    except Exception:
        # If spec is already a dict (fallback pathway), use as-is
        spec_dict = spec if isinstance(spec, dict) else {}

    if spec_dict.get("game_type") == "3D":
        result = build_3d_game(spec_dict)
    else:
        result = build_2d_game(spec_dict)

    print("=== Generated Project Summary ===")
    print(json.dumps(result, indent=2))
    print("Files saved to src/outputs/ (check saved_to in output).")


def main():
    parser = argparse.ArgumentParser(description="GameShaper-AI CLI")
    parser.add_argument("--idea", "-i", type=str, required=True, help="Text idea describing a game.")
    parser.add_argument("--no-llm", dest="use_llm", action="store_false", help="Disable LLM and use heuristics.")
    args = parser.parse_args()

    try:
        run(args.idea, use_llm=args.use_llm)
    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
