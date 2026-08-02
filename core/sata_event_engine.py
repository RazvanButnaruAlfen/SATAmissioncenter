from __future__ import annotations

from datetime import date
import random
import time
from typing import Any

import streamlit as st

from components.recovered_packets.engine import register_action
from components.recovered_packets.storage import pending_packet


STATE_KEY = "sata_event_engine_state"

ACTIVE_DROP_CHANCE = 0.20
PASSIVE_DROP_CHANCE = 0.20
PASSIVE_MIN_SECONDS = 45
PASSIVE_CHECK_INTERVAL_SECONDS = 30
EVENT_COOLDOWN_SECONDS = 75
MAX_EVENTS_PER_SESSION = 4


MICRO_EVENTS = [
    {
        "title": "OBSERVAȚIE NEPLANIFICATĂ",
        "text": "Alexandra este încă în aplicație. Curiozitatea funcționează în parametri normali.",
        "icon": "👀",
    },
    {
        "title": "ZGOMOT COSMIC",
        "text": "S.A.T.A. a detectat un semnal neobișnuit. Era doar un gând care se plimba fără destinație.",
        "icon": "📡",
    },
    {
        "title": "ANALIZĂ ÎN FUNDAL",
        "text": "S-au detectat mai multe scenarii mentale decât sunt necesare pentru funcționarea aplicației.",
        "icon": "🧠",
    },
    {
        "title": "VERIFICARE OPERATOR",
        "text": "Operatorul nu a apăsat nimic de ceva timp. Există două posibilități: citește sau se gândește. Ambele sunt acceptabile.",
        "icon": "🔎",
    },
    {
        "title": "FALSĂ ALARMĂ",
        "text": "Un pachet necunoscut a intrat în raza de recepție a satelitului. S-a dovedit a fi o reclamă la detergent.",
        "icon": "⚠️",
    },
    {
        "title": "RAPORT INTERN",
        "text": "S.A.T.A. a încercat să fie obiectiv. Încercarea a fost abandonată din motive sentimentale.",
        "icon": "🤖",
    },
    {
        "title": "SEMNAL RECURENT",
        "text": "A fost detectată din nou expresia «vedem». Traducerea rămâne în lucru.",
        "icon": "📶",
    },
    {
        "title": "ACTIVITATE SUSPECTĂ",
        "text": "Telefonul pare să fie ținut în mână. Sistemul refuză, pentru moment, să tragă concluzii pripite.",
        "icon": "📱",
    },
    {
        "title": "CORECȚIE AUTOMATĂ",
        "text": "Încrederea sistemului a ajuns la 103%. Valoarea a fost redusă discret înainte să observe cineva.",
        "icon": "🛠️",
    },
    {
        "title": "NOTĂ SATELIT",
        "text": "Nu s-a întâmplat nimic important. S.A.T.A. a considerat că merită raportat.",
        "icon": "🛰️",
    },
]


def _default_state(now: float) -> dict[str, Any]:
    return {
        "session_started_at": now,
        "last_passive_check_at": now,
        "last_event_at": 0.0,
        "events_shown": 0,
        "pending_micro_event": None,
        "micro_history": [],
    }


def get_event_state() -> dict[str, Any]:
    now = time.time()
    state = st.session_state.get(STATE_KEY)

    if not isinstance(state, dict):
        state = _default_state(now)
        st.session_state[STATE_KEY] = state

    return state


def _can_show_event(state: dict[str, Any], now: float) -> bool:
    if int(state.get("events_shown", 0)) >= MAX_EVENTS_PER_SESSION:
        return False

    last_event = float(state.get("last_event_at", 0.0))
    return now - last_event >= EVENT_COOLDOWN_SECONDS


def _select_micro_event(
    state: dict[str, Any],
    rng: random.Random,
) -> dict[str, str]:
    history = list(state.get("micro_history", []))
    recent = set(history[-4:])
    available = [
        event for event in MICRO_EVENTS
        if event["text"] not in recent
    ]

    if not available:
        available = MICRO_EVENTS

    event = rng.choice(available)
    history.append(event["text"])
    state["micro_history"] = history[-8:]
    return event


def _mark_event_shown(state: dict[str, Any], now: float) -> None:
    state["last_event_at"] = now
    state["events_shown"] = int(state.get("events_shown", 0)) + 1


def notify_active_action(
    *,
    today: date,
    trigger: str,
    rng: random.Random | None = None,
) -> None:
    """20% chance after an active interaction.

    Half of successful rolls attempt a recovered packet. The other half
    create a small S.A.T.A. interruption.
    """
    state = get_event_state()
    now = time.time()
    random_source = rng or random.SystemRandom()

    if not _can_show_event(state, now):
        return

    if random_source.random() >= ACTIVE_DROP_CHANCE:
        return

    if random_source.random() < 0.65:
        packet = register_action(
            today=today,
            trigger=trigger,
            rng=random_source,
            force_drop=True,
        )
        if packet is not None:
            _mark_event_shown(state, now)
            return

    state["pending_micro_event"] = _select_micro_event(
        state,
        random_source,
    )
    _mark_event_shown(state, now)


def check_passive_time(
    *,
    today: date,
    rng: random.Random | None = None,
) -> None:
    """Check whether S.A.T.A. should intervene while the app is open."""
    state = get_event_state()
    now = time.time()
    random_source = rng or random.SystemRandom()

    elapsed = now - float(state.get("session_started_at", now))
    since_check = now - float(state.get("last_passive_check_at", now))

    if elapsed < PASSIVE_MIN_SECONDS:
        return
    if since_check < PASSIVE_CHECK_INTERVAL_SECONDS:
        return

    state["last_passive_check_at"] = now

    if not _can_show_event(state, now):
        return
    if pending_packet(today) is not None:
        return
    if state.get("pending_micro_event") is not None:
        return
    if random_source.random() >= PASSIVE_DROP_CHANCE:
        return

    if random_source.random() < 0.55:
        packet = register_action(
            today=today,
            trigger="passive_time",
            rng=random_source,
            force_drop=True,
        )
        if packet is not None:
            _mark_event_shown(state, now)
            return

    state["pending_micro_event"] = _select_micro_event(
        state,
        random_source,
    )
    _mark_event_shown(state, now)


def pending_micro_event() -> dict[str, str] | None:
    return get_event_state().get("pending_micro_event")


def dismiss_micro_event() -> None:
    get_event_state()["pending_micro_event"] = None
