from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "intimacy"


def _load_json(filename: str) -> list[dict[str, Any]]:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)

    if not isinstance(value, list):
        raise ValueError(f"{filename} trebuie să conțină o listă.")
    return value


@lru_cache(maxsize=1)
def load_anagrams() -> tuple[dict[str, Any], ...]:
    return tuple(_load_json("anagrams.json"))


@lru_cache(maxsize=1)
def load_pre_meeting_packets() -> tuple[dict[str, Any], ...]:
    return tuple(_load_json("pre_meeting_packets.json"))

@lru_cache(maxsize=1)
def load_memory_questions() -> tuple[dict[str, Any], ...]:
    return tuple(_load_json("memory_questions.json"))

