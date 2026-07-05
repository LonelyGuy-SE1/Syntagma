import json
import os

from httpx import Client
from dotenv import load_dotenv

load_dotenv("../.env")

URL   = os.environ["OPENROUTER_URL"]
KEY   = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ["OPENROUTER_MODEL"]

def call(system: str, user: str) -> dict:
    with Client(timeout=120) as c:
        r = c.post(URL, headers={"Authorization": f"Bearer {KEY}"}, json={
            "model": MODEL,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        })
        r.raise_for_status()
        data = r.json()
        if "choices" not in data:
            raise RuntimeError(f"OpenRouter response missing choices: {data.get('error') or data}")
        text = data["choices"][0]["message"]["content"]
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)


def stream_chat(system: str, messages: list[dict]):
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, *messages],
        "stream": True,
    }
    with Client(timeout=120) as client:
        with client.stream("POST", URL, headers={"Authorization": f"Bearer {KEY}"}, json=payload) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                token = _stream_token(line)
                if token:
                    yield token


def _stream_token(line: str) -> str:
    if not line or line.startswith(":"):
        return ""
    if not line.startswith("data:"):
        return ""
    data = line.removeprefix("data:").strip()
    if data == "[DONE]":
        return ""
    chunk = json.loads(data)
    choice = (chunk.get("choices") or [{}])[0]
    delta = choice.get("delta") or {}
    return delta.get("content") or ""
