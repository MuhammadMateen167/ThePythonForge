# Minimal OpenAI service wrapper. Uses environment variable OPENAI_API_KEY.
# This file uses the OpenAI python library - update as needed to match your installed version.
import os
import json
import requests
import datetime

OPENROUTER_KEY = os.getenv("OPEN_ROUTER_API", "")
if not OPENROUTER_KEY:
    # In development this will still run but will return an error when contacting OpenAI.
    pass

CHAT_LOG_FILE = "chat_log.jsonl"  # File to store chats


def log_chat(user_prompt: str, assistant_reply: str, path=CHAT_LOG_FILE):
    """Append one user→assistant exchange to a JSONL log file."""
    record = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user": user_prompt,
        "assistant": assistant_reply,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def get_ai_response(prompt: str) -> str:
    if not OPENROUTER_KEY:
        raise RuntimeError(
            "OpenRouter API key not set. Set OPENROUTER_KEY env variable."
        )

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    messages = [
        {
            "role": "system",
            "content": "You are Nova — a nice, helpful assistant created by Mateen. Be playful, and helpful.",
        },
        {"role": "user", "content": prompt},
    ]
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800,
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        reply = r.json()["choices"][0]["message"]["content"]

        # Log the chat to file
        log_chat(prompt, reply)

        return reply
    except requests.exceptions.HTTPError as e:
        # Safe debug info
        return f"Upstream API error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
