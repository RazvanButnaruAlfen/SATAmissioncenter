from __future__ import annotations

from datetime import date
import html

import streamlit as st

from core.recovered_packet_engine import (
    decrypt_pending_packet,
    pending_packet,
)


def _render_packet(packet: dict) -> None:
    title = html.escape(str(packet.get("title", "PACHET RECUPERAT")))
    content = html.escape(str(packet.get("content", "")))
    comment = html.escape(str(packet.get("comment", "")))
    icon = html.escape(str(packet.get("icon", "📡")))
    packet_id = html.escape(str(packet.get("id", "UNKNOWN")))

    st.markdown(
        f"""
        <style>
        .packet-card {{
            margin-top:14px;
            padding:22px;
            border-radius:17px;
            color:white;
            text-align:center;
            background:
                radial-gradient(circle at 85% 5%,rgba(255,112,184,.14),transparent 35%),
                linear-gradient(145deg,#0b1722,#152636);
            border:1px solid #41647a;
            box-shadow:0 0 24px rgba(54,174,245,.10);
        }}
        .packet-id {{
            color:#63bdf4;
            font-size:.73rem;
            font-weight:900;
            letter-spacing:.12em;
        }}
        .packet-icon {{
            margin-top:.55rem;
            font-size:2.6rem;
        }}
        .packet-title {{
            margin-top:.35rem;
            color:#ffd98d;
            font-size:clamp(1.25rem,5vw,1.8rem);
            font-weight:950;
        }}
        .packet-content {{
            margin:1rem auto 0;
            max-width:760px;
            font-size:1.04rem;
            line-height:1.55;
            font-weight:700;
        }}
        .packet-comment {{
            margin-top:1rem;
            color:#9db0bd;
            font-size:.82rem;
            line-height:1.4;
        }}
        </style>

        <div class="packet-card">
          <div class="packet-id">PACHET {packet_id} • DECRIPTARE FINALIZATĂ</div>
          <div class="packet-icon">{icon}</div>
          <div class="packet-title">{title}</div>
          <div class="packet-content">{content}</div>
          <div class="packet-comment">S.A.T.A.: {comment}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recovered_packet(today: date) -> None:
    packet = pending_packet(today)

    if packet is not None:
        st.markdown(
            """
            <style>
            .packet-alert {
                margin-top:14px;
                padding:18px;
                border-radius:15px;
                background:linear-gradient(135deg,#151021,#25142d);
                border:1px solid #71426e;
                color:white;
                text-align:center;
            }
            .packet-alert-title {
                color:#ff91c6;
                font-size:.78rem;
                font-weight:900;
                letter-spacing:.12em;
            }
            .packet-alert-main {
                margin-top:.45rem;
                font-size:1.25rem;
                font-weight:950;
            }
            .packet-alert-copy {
                margin-top:.4rem;
                color:#bca9bf;
            }
            </style>
            <div class="packet-alert">
              <div class="packet-alert-title">TRANSMISIE SATELIT NECUNOSCUTĂ</div>
              <div class="packet-alert-main">📡 Pachet criptat interceptat</div>
              <div class="packet-alert-copy">
                Originea și utilitatea pachetului nu au putut fi stabilite.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔓 DECRIPTEAZĂ PACHETUL",
            use_container_width=True,
            type="primary",
            key="decrypt_recovered_packet",
        ):
            decrypted = decrypt_pending_packet(today)
            if decrypted is not None:
                st.session_state["sata_last_decrypted_packet"] = decrypted
            st.rerun()

    last_packet = st.session_state.pop("sata_last_decrypted_packet", None)
    if last_packet is not None:
        _render_packet(last_packet)
