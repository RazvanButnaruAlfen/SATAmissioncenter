from __future__ import annotations

from datetime import date
import random
import unicodedata
from typing import Any

import streamlit as st

from .data import load_anagrams, load_memory_questions, load_pre_meeting_packets


STATE_KEY = "sata_pink_archives"


def _default_state(today: date) -> dict[str, Any]:
    return {
        "date": today.isoformat(),
        "puzzle": None,
        "solved": False,
        "reward": None,
        "history": [],
        "attempts": 0,
        "feedback": None,
        "quiz_history": [],
    }


def get_state(today: date) -> dict[str, Any]:
    state = st.session_state.get(STATE_KEY)
    if not isinstance(state, dict) or state.get("date") != today.isoformat():
        state = _default_state(today)
        st.session_state[STATE_KEY] = state
    return state


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.strip().upper())
    return "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
        and character.isalpha()
    )


def _scramble(word: str, rng: random.Random) -> str:
    letters = list(word.replace(" ", ""))
    original = "".join(letters)
    for _ in range(12):
        rng.shuffle(letters)
        candidate = "".join(letters)
        if candidate != original:
            return candidate
    return "".join(reversed(letters))


def create_puzzle(
    today: date,
    *,
    force_type: str | None = None,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    state = get_state(today)
    random_source = rng or random.SystemRandom()
    puzzle_type = force_type or random_source.choice(("anagram", "frequency", "quiz"))

    if puzzle_type == "anagram":
        item = random_source.choice(load_anagrams())
        puzzle = {
            "type": "anagram",
            "word": item["word"],
            "scrambled": _scramble(item["word"], random_source),
            "hint": item["hint"],
            "level": item["level"],
        }
    elif puzzle_type == "frequency":
        target = random_source.randint(28, 92)
        puzzle = {
            "type": "frequency",
            "target": target,
            "level": random_source.choice(("GREEN", "PINK", "PINK", "RED")),
        }
    else:
        questions = list(load_memory_questions())
        recent = set(state.get("quiz_history", [])[-4:])
        available = [
            question for question in questions
            if question["id"] not in recent
        ]
        if not available:
            available = questions

        question = random_source.choice(available)
        answers = list(enumerate(question["answers"]))
        random_source.shuffle(answers)

        puzzle = {
            "type": "quiz",
            "question_id": question["id"],
            "category": question["category"],
            "question": question["question"],
            "answers": [answer for _, answer in answers],
            "correct": next(
                new_index
                for new_index, (original_index, _) in enumerate(answers)
                if original_index == int(question["correct"])
            ),
            "success": question["success"],
            "failure": question["failure"],
            "level": question["difficulty"],
        }

    state["puzzle"] = puzzle
    state["solved"] = False
    state["reward"] = None
    state["attempts"] = 0
    state["feedback"] = None
    return puzzle


def current_puzzle(today: date) -> dict[str, Any]:
    state = get_state(today)
    if state.get("puzzle") is None:
        return create_puzzle(today)
    return state["puzzle"]


def _choose_reward(state: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    packets = list(load_pre_meeting_packets())
    recent = set(state.get("history", [])[-6:])
    available = [packet for packet in packets if packet["id"] not in recent]
    if not available:
        available = packets
    return rng.choice(available)


def unlock_reward(
    today: date,
    *,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    state = get_state(today)
    random_source = rng or random.SystemRandom()
    reward = _choose_reward(state, random_source)
    history = list(state.get("history", []))
    history.append(reward["id"])
    state["history"] = history[-12:]
    state["reward"] = reward
    state["solved"] = True
    state["feedback"] = None
    return reward


def submit_anagram(today: date, answer: str) -> bool:
    state = get_state(today)
    puzzle = current_puzzle(today)
    state["attempts"] = int(state.get("attempts", 0)) + 1

    correct = normalize_text(answer) == normalize_text(str(puzzle["word"]))
    if correct:
        unlock_reward(today)
        return True

    state["feedback"] = "Cod incorect. Literele sunt corecte; ordinea este suspectă."
    return False


def tune_frequency(today: date, value: int) -> bool:
    state = get_state(today)
    puzzle = current_puzzle(today)
    target = int(puzzle["target"])
    state["attempts"] = int(state.get("attempts", 0)) + 1
    delta = value - target

    if abs(delta) <= 5:
        unlock_reward(today)
        return True

    distance = abs(delta)

    if distance <= 10:
        proximity = "Ești foarte aproape de zona de blocare. "
    elif distance <= 22:
        proximity = "Semnalul devine mai clar. "
    else:
        proximity = "Semnal încă slab. "

    if delta < 0:
        state["feedback"] = proximity + "Crește frecvența."
    else:
        state["feedback"] = proximity + "Redu frecvența."
    return False



def submit_quiz(today: date, selected_index: int | None) -> bool:
    state = get_state(today)
    puzzle = current_puzzle(today)
    state["attempts"] = int(state.get("attempts", 0)) + 1

    if selected_index is None:
        state["feedback"] = "Selectează un răspuns înainte de validare."
        return False

    if int(selected_index) == int(puzzle["correct"]):
        history = list(state.get("quiz_history", []))
        history.append(str(puzzle["question_id"]))
        state["quiz_history"] = history[-8:]
        state["feedback"] = str(puzzle["success"])
        unlock_reward(today)
        return True

    state["feedback"] = str(puzzle["failure"])
    return False

def reset_transmission(
    today: date,
    *,
    force_type: str | None = None,
) -> None:
    create_puzzle(today, force_type=force_type)
