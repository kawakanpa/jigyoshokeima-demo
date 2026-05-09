"""問題の解答履歴を管理するモジュール。"""

import json
from datetime import date
from pathlib import Path

_HISTORY_FILE = Path(__file__).parent.parent / "data" / "history.json"


def _load():
    if not _HISTORY_FILE.exists():
        return {}
    try:
        return json.loads(_HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(history):
    _HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    _HISTORY_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def record_answer(question_number, correct):
    history = _load()
    key = str(question_number)
    if key not in history:
        history[key] = {"attempts": [], "wrong_count": 0, "last_attempt": None}
    today = date.today().isoformat()
    history[key]["attempts"].append({"date": today, "correct": correct})
    if not correct:
        history[key]["wrong_count"] += 1
    history[key]["last_attempt"] = today
    _save(history)


def get_wrong_numbers():
    history = _load()
    return sorted(int(k) for k, v in history.items() if v.get("wrong_count", 0) > 0)


def get_answered_numbers():
    history = _load()
    return sorted(int(k) for k in history.keys())


def get_question_stats(question_number):
    history = _load()
    return history.get(str(question_number))
