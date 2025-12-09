## Files & folders

- `src/engines/llm_client.py` — OpenAI wrapper (JSON-only responses).
- `src/prompts/prompt_processor.py` — Converts text → validated `GameSpec`.
- `src/builders/` — 2D/3D builder stubs that output JSON projects.
- `src/utils/file_saver.py` — Saves outputs to `src/outputs/`.

## Notes

- Do **not** commit your `.env` file.
- If LLM returns invalid JSON, the pipeline will automatically fall back to heuristics.
