from __future__ import annotations

import hashlib
import random

import streamlit as st

from core.mission_state import MissionState
from core.sata_memory import (
    combined_longing_score,
    has_completed_emos_scan,
    record_archive_unlock,
    register_archive_attempt,
)
from .documents import DOCUMENTS
from .messages import RECOMMENDATION
from .security import check_access
from .ui import render_denied, render_document, render_header


def _rng(state: MissionState, attempts: int) -> random.Random:
    payload = f"archives::{state.current_date.isoformat()}::{attempts}".encode("utf-8")
    return random.Random(int(hashlib.sha256(payload).hexdigest()[:12], 16))


def render_classified_archives(state: MissionState) -> None:
    render_header()

    # Remove an old "scan required" refusal once E.M.O.S. has subsequently run.
    previous_denial = st.session_state.get("archive_denial")
    if (
        previous_denial
        and has_completed_emos_scan()
        and "scanare E.M.O.S." in str(previous_denial[0])
    ):
        st.session_state["archive_denial"] = None

    if st.button("🔒 SOLICITĂ ACCES", use_container_width=True, key="archive_access"):
        attempts = register_archive_attempt()
        rng = _rng(state, attempts)
        score = combined_longing_score()
        decision = check_access(score, rng)

        if decision.granted:
            document = rng.choice(DOCUMENTS)
            st.session_state["archive_document"] = document
            st.session_state["archive_denial"] = None
            record_archive_unlock(document["id"])
        else:
            st.session_state["archive_document"] = None
            st.session_state["archive_denial"] = (decision.reason, decision.score)

    document = st.session_state.get("archive_document")
    denial = st.session_state.get("archive_denial")

    if document:
        render_document(document)
    elif denial:
        render_denied(denial[0], denial[1], RECOMMENDATION)
