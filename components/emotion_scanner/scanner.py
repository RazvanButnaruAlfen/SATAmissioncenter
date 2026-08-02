from __future__ import annotations

import hashlib
import random
import time

import streamlit as st

from core.mission_state import MissionState
from core.sata_memory import record_emos_scan
from core.sata_event_engine import notify_active_action
from .animation import overlay_html
from .config import DETECTION_DELAY, RARE_RESULT_PROBABILITY, RESULT_DELAY, SCAN_STEP_DELAY
from .messages import (
    CONNECTING_MESSAGES,
    DETECTED_MESSAGES,
    FINAL_MESSAGES,
    SCAN_MESSAGES,
    SEARCH_MESSAGES,
    STABILIZING_MESSAGES,
)
from .results import choose_result
from .ui import render_header, render_result


def _rng(state: MissionState, scan_count: int) -> random.Random:
    payload = f"{state.current_date.isoformat()}::{scan_count}".encode("utf-8")
    seed = int(hashlib.sha256(payload).hexdigest()[:12], 16)
    return random.Random(seed)


def _show(overlay, title: str, message: str, progress: int, *, detected: bool = False, delay: float = SCAN_STEP_DELAY):
    overlay.markdown(overlay_html(title, message, progress, detected=detected), unsafe_allow_html=True)
    time.sleep(delay)


def render_emotion_scanner(state: MissionState) -> None:
    render_header()

    if st.button("▶ INIȚIAZĂ SCANAREA E.M.O.S.", use_container_width=True, type="primary", key="emos_start"):
        scan_count = st.session_state.get("emos_scan_count", 0) + 1
        st.session_state["emos_scan_count"] = scan_count
        rng = _rng(state, scan_count)
        overlay = st.empty()

        _show(overlay, "INIȚIALIZARE", rng.choice(CONNECTING_MESSAGES), 8)
        _show(overlay, "CONECTARE SATELIȚI", rng.choice(CONNECTING_MESSAGES), 20)
        _show(overlay, "CĂUTARE ALEXANDRA", rng.choice(SEARCH_MESSAGES), 34)
        _show(overlay, "TRIANGULARE SEMNAL", rng.choice(SEARCH_MESSAGES), 46)
        _show(overlay, rng.choice(DETECTED_MESSAGES), rng.choice(STABILIZING_MESSAGES), 58, detected=True, delay=DETECTION_DELAY)

        scan_steps = rng.sample(SCAN_MESSAGES, k=min(4, len(SCAN_MESSAGES)))
        for progress, message in zip((68, 76, 84, 91), scan_steps):
            _show(overlay, "SCANARE ÎN PROGRES", message, progress, detected=True)

        _show(overlay, "ANALIZĂ FINALĂ", rng.choice(FINAL_MESSAGES), 97, detected=True)
        _show(overlay, "SCANARE FINALIZATĂ", "Rezultatul este pregătit. Telefonul poate fi mișcat din nou.", 100, detected=True, delay=RESULT_DELAY)
        overlay.empty()

        previous_result = st.session_state.get("emos_last_result")
        previous_title = previous_result[0] if previous_result else None
        title, text, score = choose_result(
            state.current_date,
            rng,
            RARE_RESULT_PROBABILITY,
            previous_title=previous_title,
        )
        record_emos_scan(
            score=score,
            title=title,
            text=text,
            scan_date=state.current_date.isoformat(),
        )
        notify_active_action(
            today=state.current_date,
            trigger="emos_scan",
            rng=rng,
        )

    result = st.session_state.get("emos_last_result")
    if result:
        render_result(*result)

