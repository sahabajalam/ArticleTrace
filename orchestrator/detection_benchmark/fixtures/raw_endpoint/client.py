"""Calls a hosted LLM with plain HTTP — no AI SDK import anywhere."""
import os

import requests


def complete(prompt: str) -> str:
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['KEY']}"},
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    return resp.json()["choices"][0]["message"]["content"]
