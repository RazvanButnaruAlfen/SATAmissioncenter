from __future__ import annotations

import streamlit as st

from core.sata_memory import (
    active_data_sources,
    combined_longing_score,
    snapshot,
)


def _value(value: int | None) -> str:
    return "NECALIBRAT" if value is None else f"{value}%"


def render_system_status() -> None:
    data = snapshot()
    sources = active_data_sources()
    combined = combined_longing_score()

    source_text = " + ".join(sources) if sources else "NICIO SURSĂ"
    sync_state = "SINCRONIZAT" if sources else "AȘTEAPTĂ DATE"

    st.markdown(
        f"""
        <style>
        .sync-shell {{
            margin-top:16px;
            border:1px solid #2b4d61;
            border-radius:16px;
            padding:18px;
            color:white;
            background:linear-gradient(145deg,#07131d,#0e1d29);
        }}
        .sync-head {{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            flex-wrap:wrap;
        }}
        .sync-kicker {{
            color:#63bdf4;
            font-size:.75rem;
            font-weight:900;
            letter-spacing:.12em;
        }}
        .sync-state {{
            color:#63d39b;
            font-size:.78rem;
            font-weight:900;
        }}
        .sync-grid {{
            display:grid;
            grid-template-columns:repeat(4,minmax(0,1fr));
            gap:10px;
            margin-top:14px;
        }}
        .sync-card {{
            background:#0b1722;
            border:1px solid #294454;
            border-radius:13px;
            padding:12px;
            min-width:0;
        }}
        .sync-label {{
            color:#8195a4;
            font-size:.68rem;
            margin-bottom:5px;
        }}
        .sync-value {{
            color:#f4f7fa;
            font-size:1rem;
            line-height:1.25;
            font-weight:850;
            overflow-wrap:anywhere;
        }}
        .sync-note {{
            margin-top:12px;
            color:#a9bac6;
            font-size:.82rem;
            line-height:1.4;
        }}
        @media(max-width:760px) {{
            .sync-grid {{grid-template-columns:1fr 1fr;}}
        }}
        </style>

        <div class="sync-shell">
          <div class="sync-head">
            <div class="sync-kicker">S.A.T.A. • MEMORIE OPERAȚIONALĂ COMUNĂ</div>
            <div class="sync-state">● {sync_state}</div>
          </div>

          <div class="sync-grid">
            <div class="sync-card">
              <div class="sync-label">E.M.O.S.</div>
              <div class="sync-value">{_value(data.emos_score)}</div>
            </div>
            <div class="sync-card">
              <div class="sync-label">Fricometru</div>
              <div class="sync-value">{_value(data.fear_score)}</div>
            </div>
            <div class="sync-card">
              <div class="sync-label">Coeficient combinat</div>
              <div class="sync-value">{_value(combined)}</div>
            </div>
            <div class="sync-card">
              <div class="sync-label">Încercări arhivă</div>
              <div class="sync-value">{data.archive_attempts}</div>
            </div>
          </div>

          <div class="sync-note">
            Surse active: <b>{source_text}</b>. Instrumentele schimbă date între ele
            prin metode avansate, neverificate și foarte sigure pe ele.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
