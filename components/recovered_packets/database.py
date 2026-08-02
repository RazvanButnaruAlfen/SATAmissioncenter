from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .packet_types import RecoveredPacket


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "recovered_packets"
DATA_FILES = (
    "jokes.json",
    "fun_facts.json",
    "recipes.json",
    "movies.json",
    "workouts.json",
)


@lru_cache(maxsize=1)
def load_packets() -> tuple[RecoveredPacket, ...]:
    packets: list[RecoveredPacket] = []

    for filename in DATA_FILES:
        path = DATA_DIR / filename
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8") as file:
            raw = json.load(file)

        if not isinstance(raw, list):
            raise ValueError(f"{filename} trebuie să conțină o listă.")

        packets.extend(RecoveredPacket.from_dict(item) for item in raw)

    if not packets:
        raise RuntimeError("Nu există pachete recuperabile în baza de date.")

    identifiers = [packet.id for packet in packets]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Există ID-uri duplicate în baza de date.")

    return tuple(packets)
