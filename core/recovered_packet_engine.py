from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import random
from typing import Any

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
PACKETS_FILE = BASE_DIR / "data" / "recovered_packets" / "packets.json"
STATE_KEY = "sata_recovered_packets"


def _state(today: date) -> dict[str, Any]:
    current = st.session_state.get(STATE_KEY)
    today_key = today.isoformat()

    if not isinstance(current, dict) or current.get("date") != today_key:
        current = {
            "date": today_key,
            "actions_since_packet": 0,
            "packets_today": [],
            "pending_packet": None,
            "last_trigger": None,
        }
        st.session_state[STATE_KEY] = current

    return current


def _load_packets() -> list[dict[str, Any]]:
    with PACKETS_FILE.open("r", encoding="utf-8") as file:
        content = json.load(file)

    if not isinstance(content, list):
        raise ValueError("packets.json trebuie să conțină o listă.")

    return content


def register_action(
    *,
    today: date,
    trigger: str,
    rng: random.Random | None = None,
) -> dict[str, Any] | None:
    """Potentially recover a packet after an interaction.

    The user never sees the internal rule. The probability slowly
    increases after unsuccessful actions and becomes certain after
    enough attempts, then resets.
    """
    state = _state(today)

    # Do not overwrite a packet that is waiting to be decrypted.
    if state.get("pending_packet") is not None:
        return state["pending_packet"]

    state["actions_since_packet"] = int(state["actions_since_packet"]) + 1
    attempts = int(state["actions_since_packet"])
    random_source = rng or random.SystemRandom()

    probability = min(0.72, 0.055 + max(0, attempts - 1) * 0.065)
    should_trigger = attempts >= 10 or random_source.random() < probability

    if not should_trigger:
        return None

    packets = _load_packets()
    seen_ids = set(state.get("packets_today", []))
    available = [packet for packet in packets if packet["id"] not in seen_ids]

    # If every packet has been seen today, start a fresh cycle.
    if not available:
        state["packets_today"] = []
        available = packets

    packet = random_source.choice(available)
    state["pending_packet"] = packet
    state["last_trigger"] = trigger
    state["actions_since_packet"] = 0
    return packet


def pending_packet(today: date) -> dict[str, Any] | None:
    return _state(today).get("pending_packet")


def decrypt_pending_packet(today: date) -> dict[str, Any] | None:
    state = _state(today)
    packet = state.get("pending_packet")
    if packet is None:
        return None

    seen = list(state.get("packets_today", []))
    if packet["id"] not in seen:
        seen.append(packet["id"])

    state["packets_today"] = seen
    state["pending_packet"] = None
    return packet


def packets_recovered_today(today: date) -> int:
    return len(_state(today).get("packets_today", []))
