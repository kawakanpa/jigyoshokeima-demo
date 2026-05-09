"""問題の解答履歴をセッション内のみで管理するモジュール（デモ版）。"""

from datetime import date

import streamlit as st

_KEY = "_demo_history"


def _load():
    return st.session_state.get(_KEY, {})


def _save(history):
    st.session_state[_KEY] = history


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
