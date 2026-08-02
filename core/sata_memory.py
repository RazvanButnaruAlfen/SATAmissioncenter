from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import streamlit as st


MEMORY_KEY = "sata_shared_memory"


@dataclass(frozen=True)
class MemorySnapshot:
    emos_score: int | None
    emos_title: str | None
    emos_scan_date: str | None
    fear_score: int | None
    fear_updated_at: str | None
    prediction: str | None
    archive_attempts: int
    archive_unlocked: bool
    archive_document_id: str | None


def _default_memory() -> dict[str, Any]:
    return {
        "emos_score": None,
        "emos_title": None,
        "emos_text": None,
        "emos_scan_date": None,
        "emos_scan_count": 0,
        "fear_score": None,
        "fear_updated_at": None,
        "prediction": None,
        "archive_attempts": 0,
        "archive_unlocked": False,
        "archive_document_id": None,
    }


def get_memory() -> dict[str, Any]:
    if MEMORY_KEY not in st.session_state:
        st.session_state[MEMORY_KEY] = _default_memory()
    return st.session_state[MEMORY_KEY]


def snapshot() -> MemorySnapshot:
    memory = get_memory()
    return MemorySnapshot(
        emos_score=memory.get("emos_score"),
        emos_title=memory.get("emos_title"),
        emos_scan_date=memory.get("emos_scan_date"),
        fear_score=memory.get("fear_score"),
        fear_updated_at=memory.get("fear_updated_at"),
        prediction=memory.get("prediction"),
        archive_attempts=int(memory.get("archive_attempts", 0)),
        archive_unlocked=bool(memory.get("archive_unlocked", False)),
        archive_document_id=memory.get("archive_document_id"),
    )


def record_emos_scan(
    *,
    score: int | None,
    title: str,
    text: str,
    scan_date: str,
) -> None:
    memory = get_memory()
    memory["emos_score"] = score
    memory["emos_title"] = title
    memory["emos_text"] = text
    memory["emos_scan_date"] = scan_date
    memory["emos_scan_count"] = int(memory.get("emos_scan_count", 0)) + 1

    # Keep legacy values available while the project is migrated.
    st.session_state["emos_last_score"] = score
    st.session_state["emos_last_result"] = (title, text, score)
    st.session_state["emos_last_scan_date"] = scan_date


def record_fear_score(score: int) -> None:
    normalized = max(0, min(100, int(score)))
    memory = get_memory()
    memory["fear_score"] = normalized
    memory["fear_updated_at"] = datetime.now().isoformat(timespec="seconds")
    st.session_state["fricometru_score"] = normalized


def record_prediction(text: str) -> None:
    memory = get_memory()
    memory["prediction"] = text
    st.session_state["fricometru_prediction"] = text


def register_archive_attempt() -> int:
    memory = get_memory()
    memory["archive_attempts"] = int(memory.get("archive_attempts", 0)) + 1
    st.session_state["archive_attempts"] = memory["archive_attempts"]
    return memory["archive_attempts"]


def record_archive_unlock(document_id: str) -> None:
    memory = get_memory()
    memory["archive_unlocked"] = True
    memory["archive_document_id"] = document_id


def combined_longing_score() -> int | None:
    """Combine the instruments without pretending the result is scientific.

    E.M.O.S. supplies the primary estimate. Fricometrul slightly adjusts
    it: a higher fear score is interpreted by S.A.T.A. as stronger
    emotional relevance, because the algorithms are confidently dubious.
    """
    memory = get_memory()
    emos = memory.get("emos_score")
    fear = memory.get("fear_score")

    if emos is None and fear is None:
        return None
    if emos is None:
        return max(0, min(100, 35 + round(int(fear) * 0.45)))
    if fear is None:
        return int(emos)

    combined = round(int(emos) * 0.78 + int(fear) * 0.22)
    return max(0, min(100, combined))


def active_data_sources() -> list[str]:
    memory = get_memory()
    sources: list[str] = []

    if memory.get("emos_scan_date"):
        sources.append("E.M.O.S.")
    if memory.get("fear_score") is not None:
        sources.append("FRICOMETRU.EXE")
    if int(memory.get("archive_attempts", 0)) > 0:
        sources.append("CLASSIFIED ARCHIVES")

    return sources
