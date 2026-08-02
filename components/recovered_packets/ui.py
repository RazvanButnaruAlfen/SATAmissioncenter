from __future__ import annotations

from datetime import date
import html
import time

import streamlit as st

from .packet_types import RecoveredPacket
from .storage import archive_packet, archive_packets, pending_packet


def _render_packet_card(packet: RecoveredPacket) -> None:
    packet_id = html.escape(packet.id)
    icon = html.escape(packet.icon)
    title = html.escape(packet.title)
    content = html.escape(packet.content)
    comment = html.escape(packet.comment)

    st.markdown(
        f"""
        <div class="rp-card">
          <div class="rp-id">PACHET {packet_id} • RECUPERARE COMPLETĂ</div>
          <div class="rp-icon">{icon}</div>
          <div class="rp-title">{title}</div>
          <div class="rp-content">{content}</div>
          <div class="rp-comment">S.A.T.A.: {comment}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_styles() -> None:
    st.markdown(
        """
        <style>
        .rp-alert {
            margin-top:16px;
            padding:20px;
            border-radius:17px;
            color:white;
            text-align:center;
            background:
                radial-gradient(circle at 85% 0%,rgba(255,112,184,.18),transparent 38%),
                linear-gradient(145deg,#141020,#24142e);
            border:1px solid #71426e;
            box-shadow:0 0 25px rgba(255,112,184,.09);
        }
        .rp-alert-kicker {
            color:#ff91c6;
            font-size:.76rem;
            font-weight:900;
            letter-spacing:.12em;
        }
        .rp-alert-main {
            margin-top:.5rem;
            font-size:clamp(1.25rem,5vw,1.75rem);
            font-weight:950;
        }
        .rp-alert-copy {
            margin-top:.45rem;
            color:#bca9bf;
            line-height:1.45;
        }
        .rp-card {
            margin-top:16px;
            padding:22px;
            border-radius:17px;
            color:white;
            text-align:center;
            background:
                radial-gradient(circle at 85% 5%,rgba(255,112,184,.14),transparent 35%),
                linear-gradient(145deg,#0b1722,#152636);
            border:1px solid #41647a;
            box-shadow:0 0 24px rgba(54,174,245,.10);
        }
        .rp-id {
            color:#63bdf4;
            font-size:.72rem;
            font-weight:900;
            letter-spacing:.12em;
        }
        .rp-icon {
            margin-top:.6rem;
            font-size:2.7rem;
        }
        .rp-title {
            margin-top:.35rem;
            color:#ffd98d;
            font-size:clamp(1.25rem,5vw,1.85rem);
            font-weight:950;
        }
        .rp-content {
            margin:1rem auto 0;
            max-width:760px;
            font-size:1.05rem;
            line-height:1.58;
            font-weight:700;
        }
        .rp-comment {
            margin-top:1rem;
            color:#9db0bd;
            font-size:.82rem;
            line-height:1.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_recovered_packets(today: date) -> None:
    _render_styles()
    packet = pending_packet(today)

    if packet is not None:
        st.markdown(
            """
            <div class="rp-alert">
              <div class="rp-alert-kicker">ÎNTRERUPERE SATELIT NEPLANIFICATĂ</div>
              <div class="rp-alert-main">📡 Pachet criptat interceptat</div>
              <div class="rp-alert-copy">
                Tipul și utilitatea pachetului sunt necunoscute.
                S.A.T.A. recomandă decriptarea, deși nu își asumă rezultatul.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔓 DECRIPTEAZĂ PACHETUL",
            use_container_width=True,
            type="primary",
            key="rp_decrypt",
        ):
            status = st.empty()
            bar = st.progress(0)

            steps = [
                (16, "Stabilizare semnal..."),
                (38, "Verificare integritate..."),
                (61, "Eliminare zgomot satelit..."),
                (83, "Reconstrucție fragment..."),
                (100, "Decriptare finalizată."),
            ]

            for progress, message in steps:
                status.info(message)
                bar.progress(progress)
                time.sleep(0.35)

            status.empty()
            bar.empty()
            archive_packet(today, packet)
            st.session_state["rp_just_opened"] = packet.to_dict()
            st.rerun()

    opened = st.session_state.pop("rp_just_opened", None)
    if opened:
        _render_packet_card(RecoveredPacket.from_dict(opened))

    recovered = archive_packets(today)
    if recovered:
        with st.expander(
            f"📂 Pachete recuperate astăzi ({len(recovered)})",
            expanded=False,
        ):
            for item in reversed(recovered):
                st.markdown(
                    f"**{item.icon} {item.title}**  \n"
                    f"{item.content}  \n"
                    f"*S.A.T.A.: {item.comment}*"
                )
                st.divider()
