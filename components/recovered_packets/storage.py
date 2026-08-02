from __future__ import annotations

from datetime import date
from typing import Any

import streamlit as st

from .packet_types import RecoveredPacket


STATE_KEY = "sata_recovered_packet_state"


def get_state(today: date) -> dict[str, Any]:
    today_key = today.isoformat()
    state = st.session_state.get(STATE_KEY)

    if not isinstance(state, dict) or state.get("date") != today_key:
        state = {
            "date": today_key,
            "actions_since_packet": 0,
            "seen_today": [],
            "pending": None,
            "archive": [],
            "last_trigger": None,
        }
        st.session_state[STATE_KEY] = state

    return state


def pending_packet(today: date) -> RecoveredPacket | None:
    raw = get_state(today).get("pending")
    return RecoveredPacket.from_dict(raw) if raw else None


def set_pending(
    today: date,
    packet: RecoveredPacket,
    *,
    trigger: str,
) -> None:
    state = get_state(today)
    state["pending"] = packet.to_dict()
    state["last_trigger"] = trigger


def clear_pending(today: date) -> None:
    get_state(today)["pending"] = None


def increment_actions(today: date) -> int:
    state = get_state(today)
    state["actions_since_packet"] = int(
        state.get("actions_since_packet", 0)
    ) + 1
    return state["actions_since_packet"]


def reset_actions(today: date) -> None:
    get_state(today)["actions_since_packet"] = 0


def seen_ids(today: date) -> set[str]:
    return set(get_state(today).get("seen_today", []))


def archive_packet(today: date, packet: RecoveredPacket) -> None:
    state = get_state(today)

    seen = list(state.get("seen_today", []))
    if packet.id not in seen:
        seen.append(packet.id)
    state["seen_today"] = seen

    archive = list(state.get("archive", []))
    if not any(item.get("id") == packet.id for item in archive):
        archive.append(packet.to_dict())
    state["archive"] = archive

    state["pending"] = None


def archive_packets(today: date) -> list[RecoveredPacket]:
    return [
        RecoveredPacket.from_dict(item)
        for item in get_state(today).get("archive", [])
    ]
