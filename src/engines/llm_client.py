"""
LLM client wrapper using OpenAI. Expects JSON-only responses from the model.
Place this file at src/engines/llm_client.py
"""
import json
from typing import Any, Dict
from dotenv import load_dotenv
import os
import openai

load_dotenv()


class LLMClient:
    """
    Simple wrapper around OpenAI ChatCompletion.
    Exposes generate_json(prompt: str) -> Dict[str, Any]
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Copy .env.example -> .env and set your key.")
        openai.api_key = api_key
        self.model = model

    def generate_json(self, prompt: str, temperature: float = 0.2) -> Dict[str, Any]:
        """
        Send a prompt and return parsed JSON response.
        Raises ValueError if JSON can't be parsed.
        """
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a JSON-only generator. Respond ONLY with valid JSON. "
                        "Do not include any explanatory text, markdown, or surrounding backticks."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=800,
        )

        # Support different response shapes depending on SDK
        try:
            content = resp["choices"][0]["message"]["content"]
        except Exception:
            try:
                content = resp.choices[0].message["content"]
            except Exception:
                raise ValueError(f"Unexpected OpenAI response shape: {resp!r}")

        # Try to parse as JSON. If LLM returned things like code fences, strip them.
        raw = content.strip()
        # Remove code fences if present
        if raw.startswith("```") and raw.endswith("```"):
            # get inner content
            raw = "\n".join(raw.split("\n")[1:-1]).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Try to find first '{' and last '}' to salvage JSON
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = raw[start:end+1]
                try:
                    return json.loads(candidate)
                except Exception:
                    pass
            raise ValueError(f"LLM returned invalid JSON: {raw[:400]}...") from None
