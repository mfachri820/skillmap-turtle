import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_openrouter_key():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        raise RuntimeError(".env file not found. Place your OpenRouter API key in the project root.")

    raw_value = env_path.read_text(encoding="utf-8").strip()
    if not raw_value:
        raise RuntimeError("OpenRouter API key is missing from .env.")

    if "=" in raw_value:
        # Support either bare key or KEY=VALUE format
        for line in raw_value.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                if key.strip().upper() in {"OPENROUTER_API_KEY", "API_KEY", "OPENAI_API_KEY"}:
                    return value.strip()
        # fallback if no recognized key name is present
        return raw_value.split("=", 1)[-1].strip()
    return raw_value


def decode_user_input_to_skills(user_input, skill_keyword_map):
    if not user_input:
        return []

    api_key = load_openrouter_key()
    canonical_skills = sorted(set(skill_keyword_map.values()))
    prompt = (
        "Kamu adalah asisten peta karier. "
        "User memberi teks deskriptif tentang minat, pengalaman, atau preferensi mereka. "
        "Dari teks tersebut, pilih skill yang paling relevan dari daftar skill berikut ini: "
        + ", ".join(canonical_skills)
        + ".\n"
        "Kembalikan hanya JSON array dari nama-nama skill yang ada di daftar tersebut, tanpa penjelasan tambahan. "
        f"User text: \"{user_input}\""
    )

    body = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {"role": "system", "content": "You are a helper that extracts normalized career skills from user text."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "OpenRouter-Key": api_key,
        "User-Agent": "SkillMapAI/1.0",
    }

    req = Request(OPENROUTER_URL, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urlopen(req, timeout=30) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"OpenRouter response error: {exc.code} {exc.reason} - {body_text}")
    except URLError as exc:
        raise RuntimeError(f"Could not reach OpenRouter: {exc.reason}")

    choices = response_data.get("choices") or []
    if not choices:
        raise RuntimeError("OpenRouter did not return a valid completion.")

    text = choices[0].get("message", {}).get("content", "")
    try:
        decoded = json.loads(text.strip())
    except Exception:
        decoded = []
        for line in text.splitlines():
            try:
                decoded = json.loads(line.strip())
                break
            except Exception:
                continue

    if not isinstance(decoded, list):
        raise RuntimeError("OpenRouter response could not be parsed as a JSON array of skills.")

    return [skill for skill in decoded if skill in canonical_skills]
