from __future__ import annotations

from datetime import date
import html

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from core.sata_event_engine import (
    check_passive_time,
    dismiss_micro_event,
    pending_micro_event,
)
from components.recovered_packets import render_recovered_packets


def render_sata_events(today: date) -> None:
    # A discreet rerun lets passive events appear while the user reads.
    st_autorefresh(
        interval=15_000,
        limit=None,
        key="sata_passive_event_timer",
    )

    check_passive_time(today=today)
    event = pending_micro_event()

    if event is not None:
        title = html.escape(str(event["title"]))
        text = html.escape(str(event["text"]))
        icon = html.escape(str(event["icon"]))

        st.markdown(
            f"""
            <style>
            .sata-event {{
                margin:16px 0;
                padding:22px;
                border-radius:17px;
                text-align:center;
                color:white;
                background:
                    radial-gradient(circle at 80% 0%,rgba(255,112,184,.15),transparent 38%),
                    linear-gradient(145deg,#0a1722,#132b3b);
                border:1px solid #41647a;
                box-shadow:0 0 24px rgba(54,174,245,.10);
            }}
            .sata-event-kicker {{
                color:#63bdf4;
                font-size:.74rem;
                font-weight:900;
                letter-spacing:.12em;
            }}
            .sata-event-icon {{
                margin-top:.55rem;
                font-size:2.6rem;
            }}
            .sata-event-title {{
                margin-top:.3rem;
                color:#ffd98d;
                font-size:clamp(1.25rem,5vw,1.8rem);
                font-weight:950;
            }}
            .sata-event-text {{
                max-width:760px;
                margin:.85rem auto 0;
                font-size:1.04rem;
                line-height:1.55;
                font-weight:700;
            }}
            </style>

            <div class="sata-event">
              <div class="sata-event-kicker">S.A.T.A. • INTERVENȚIE SPONTANĂ</div>
              <div class="sata-event-icon">{icon}</div>
              <div class="sata-event-title">{title}</div>
              <div class="sata-event-text">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "✓ AM LUAT LA CUNOȘTINȚĂ",
            use_container_width=True,
            key="dismiss_sata_micro_event",
        ):
            dismiss_micro_event()
            st.rerun()

    render_recovered_packets(today)
