import json


def parse_serial_line(line: str):
    """Interpreta dados recebidos do Arduino e converte em escolha booleana."""
    if not line:
        return None

    raw = line.strip()

    # Suporta formato JSON: {"choice": true}
    if raw.startswith("{") and raw.endswith("}"):
        try:
            payload = json.loads(raw)
            choice = payload.get("choice")
            if isinstance(choice, bool):
                return {"choice": choice}
        except json.JSONDecodeError:
            return None

    normalized = raw.upper().replace(" ", "")

    if normalized.startswith("BUTTON1:") or normalized.startswith("BUTTON1="):
        status = normalized.split(":", 1)[1] if ":" in normalized else normalized.split("=", 1)[1]
        if status == "HIGH":
            return {"choice": False}

    if normalized.startswith("BUTTON2:") or normalized.startswith("BUTTON2="):
        status = normalized.split(":", 1)[1] if ":" in normalized else normalized.split("=", 1)[1]
        if status == "HIGH":
            return {"choice": True}

    if normalized.startswith("CHOICE:") or normalized.startswith("CHOICE="):
        status = normalized.split(":", 1)[1] if ":" in normalized else normalized.split("=", 1)[1]
        if status in {"1", "TRUE", "SIM", "YES"}:
            return {"choice": True}
        if status in {"0", "FALSE", "NAO", "NÃO", "NO"}:
            return {"choice": False}

    return None
