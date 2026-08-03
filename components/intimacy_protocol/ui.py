from __future__ import annotations

from datetime import date
import html
import time

import streamlit as st

from core.app_config import RELEASE_MODE
from core.mission_state import MissionState
from .frequency_slider import frequency_slider
from .engine import (
    current_puzzle,
    get_state,
    reset_transmission,
    submit_anagram,
    submit_quiz,
    tune_frequency,
)


def _styles() -> None:
    st.markdown(
        """
        <style>
        .pink-shell {
            margin-top:18px;
            padding:22px;
            border-radius:19px;
            color:white;
            background:
                radial-gradient(circle at 90% 0%,rgba(255,55,145,.22),transparent 35%),
                linear-gradient(145deg,#160c19,#291126 55%,#101824);
            border:1px solid #85456d;
            box-shadow:0 0 28px rgba(255,76,155,.12);
        }
        .pink-kicker {
            color:#ff83bd;
            font-size:.76rem;
            font-weight:950;
            letter-spacing:.13em;
        }
        .pink-title {
            margin-top:.35rem;
            font-size:clamp(1.65rem,5vw,2.35rem);
            font-weight:950;
        }
        .pink-copy {
            margin-top:.55rem;
            color:#d7bfd0;
            line-height:1.5;
        }
        .pink-level {
            display:inline-block;
            margin-top:12px;
            padding:6px 10px;
            border:1px solid #a95b84;
            border-radius:999px;
            color:#ffd3e7;
            font-size:.76rem;
            font-weight:900;
            letter-spacing:.08em;
        }
        .anagram {
            margin:18px 0 10px;
            text-align:center;
            font-size:clamp(2rem,8vw,3.4rem);
            font-weight:950;
            letter-spacing:.22em;
            color:#ffd98d;
            overflow-wrap:anywhere;
        }
        .pink-hint {
            text-align:center;
            color:#af9aaa;
            font-size:.88rem;
            margin-bottom:8px;
        }
        .reward-card {
            margin-top:16px;
            padding:23px;
            border-radius:17px;
            color:white;
            background:linear-gradient(145deg,#0c1822,#251426);
            border:1px solid #8b5372;
            text-align:center;
        }
        .reward-icon {font-size:2.8rem;}
        .reward-meta {
            color:#ff8fc3;
            font-size:.75rem;
            font-weight:950;
            letter-spacing:.1em;
        }
        .reward-title {
            margin-top:.5rem;
            font-size:clamp(1.35rem,5vw,1.9rem);
            font-weight:950;
            color:#ffd9e9;
        }
        .reward-content {
            margin:1rem auto 0;
            max-width:780px;
            white-space:pre-line;
            line-height:1.62;
            font-size:1.04rem;
            font-weight:650;
        }
        .reward-comment {
            margin-top:1rem;
            color:#a995a4;
            font-size:.84rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _decrypt_animation() -> None:
    status = st.empty()
    progress = st.progress(0)
    for value, message in [
        (18, "Stabilizare canal privat..."),
        (41, "Verificare nivel PINK..."),
        (67, "Eliminare filtre de pudoare..."),
        (88, "Reconstrucție protocol Venus..."),
        (100, "Acces autorizat."),
    ]:
        status.info(message)
        progress.progress(value)
        time.sleep(0.28)
    status.empty()
    progress.empty()


def _render_reward(reward: dict) -> None:
    st.markdown(
        f"""
        <div class="reward-card">
          <div class="reward-meta">
            {html.escape(str(reward["id"]))} • {html.escape(str(reward["category"]))}
            • {html.escape(str(reward["level"]))} CLEARANCE
          </div>
          <div class="reward-icon">{html.escape(str(reward["icon"]))}</div>
          <div class="reward-title">{html.escape(str(reward["title"]))}</div>
          <div class="reward-content">{html.escape(str(reward["content"])).replace(chr(92) + "n", "<br>").replace(chr(10), "<br>")}</div>
          <div class="reward-comment">S.A.T.A.: {html.escape(str(reward["comment"]))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_intimacy_protocol(state: MissionState) -> None:
    _styles()
    today = state.current_date
    memory = get_state(today)
    puzzle = current_puzzle(today)

    st.markdown(
        f"""
        <div class="pink-shell">
          <div class="pink-kicker">S.A.T.A. • PINK ARCHIVES</div>
          <div class="pink-title">🔐 Transmisie intimă criptată</div>
          <div class="pink-copy">
            Un pachet despre atracție, anticipare și pasiune a fost interceptat.
            Accesul necesită rezolvarea unui test de validare.
          </div>
          <div class="pink-level">{html.escape(str(puzzle["level"]))} CLEARANCE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if memory.get("solved") and memory.get("reward"):
        _render_reward(memory["reward"])
        if st.button(
            "📡 INTERCEPTEAZĂ O NOUĂ TRANSMISIE",
            use_container_width=True,
            key="pink_new_transmission",
        ):
            reset_transmission(today)
            st.rerun()
        return

    if puzzle["type"] == "anagram":
        st.markdown(
            f'<div class="anagram">{" ".join(html.escape(x) for x in puzzle["scrambled"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="pink-hint">Indiciu: {html.escape(str(puzzle["hint"]))}</div>',
            unsafe_allow_html=True,
        )
        answer = st.text_input(
            "Introdu cuvântul decriptat",
            key="pink_anagram_answer",
            placeholder="Scrie răspunsul aici...",
        )
        if st.button(
            "🔓 VALIDEAZĂ CUVÂNTUL",
            use_container_width=True,
            type="primary",
            key="pink_submit_anagram",
        ):
            if submit_anagram(today, answer):
                _decrypt_animation()
                st.rerun()

    elif puzzle["type"] == "frequency":
        st.markdown(
            '<div class="pink-hint" style="margin-top:18px">'
            'Reglează frecvența până când semnalul intră în zona de blocare. '
            'S.A.T.A. îți va spune numai direcția.</div>',
            unsafe_allow_html=True,
        )
        value = frequency_slider(
            target=int(puzzle["target"]),
            value=int(st.session_state.get("pink_frequency_value", 50)),
            tolerance=5,
            key="pink_frequency_audio_slider",
        )
        st.session_state["pink_frequency_value"] = int(value)

        if st.button(
            "📶 VERIFICĂ ȘI BLOCHEAZĂ SEMNALUL",
            use_container_width=True,
            type="primary",
            key="pink_tune_frequency",
        ):
            if tune_frequency(today, value):
                _decrypt_animation()
                st.rerun()


    else:
        st.markdown(
            f"""
            <div class="reward-card" style="text-align:left">
              <div class="reward-meta">
                MEMORY ARCHIVES • {html.escape(str(puzzle["category"]))}
              </div>
              <div class="reward-title" style="text-align:left">
                🗂 Verificare de memorie personală
              </div>
              <div class="reward-content" style="text-align:left">
                {html.escape(str(puzzle["question"]))}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_answer = st.radio(
            "Selectează răspunsul corect",
            options=list(range(len(puzzle["answers"]))),
            format_func=lambda index: str(puzzle["answers"][index]),
            index=None,
            key=f'pink_quiz_{puzzle["question_id"]}',
        )

        if st.button(
            "🗂 VALIDEAZĂ MEMORIA",
            use_container_width=True,
            type="primary",
            key="pink_submit_quiz",
        ):
            if submit_quiz(today, selected_answer):
                _decrypt_animation()
                st.rerun()

    feedback = get_state(today).get("feedback")
    if feedback:
        st.warning(feedback)

    if not RELEASE_MODE:
        with st.expander("🛠 PINK ARCHIVES — DEV TOOLS"):
            col1, col2, col3, col4 = st.columns(4)
            if col1.button("Forțează anagramă", use_container_width=True):
                reset_transmission(today, force_type="anagram")
                st.rerun()
            if col2.button("Forțează frecvență", use_container_width=True):
                reset_transmission(today, force_type="frequency")
                st.rerun()
            if col3.button("Forțează quiz", use_container_width=True):
                reset_transmission(today, force_type="quiz")
                st.rerun()
            if col4.button("Reset", use_container_width=True):
                reset_transmission(today)
                st.rerun()
