from __future__ import annotations

import hashlib
import random

import streamlit as st

from core.mission_state import MissionState
from .documents import DOCUMENTS
from .messages import RECOMMENDATION
from .security import check_access
from .ui import render_denied, render_document, render_header


def _rng(state: MissionState, attempts: int) -> random.Random:
    payload = f"archives::{state.current_date.isoformat()}::{attempts}".encode("utf-8")
    return random.Random(int(hashlib.sha256(payload).hexdigest()[:12], 16))


def render_classified_archives(state: MissionState) -> None:
    render_header()

    if st.button("🔒 SOLICITĂ ACCES", use_container_width=True, key="archive_access"):
        attempts = st.session_state.get("archive_attempts", 0) + 1
        st.session_state["archive_attempts"] = attempts
        rng = _rng(state, attempts)
        score = st.session_state.get("emos_last_score")
        decision = check_access(score, rng)

        if decision.granted:
            st.session_state["archive_document"] = rng.choice(DOCUMENTS)
            st.session_state["archive_denial"] = None
        else:
            st.session_state["archive_document"] = None
            st.session_state["archive_denial"] = (decision.reason, decision.score)

    document = st.session_state.get("archive_document")
    denial = st.session_state.get("archive_denial")

    if document:
        render_document(document)
    elif denial:
        render_denied(denial[0], denial[1], RECOMMENDATION)
