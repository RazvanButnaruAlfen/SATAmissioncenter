import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <style>
        .emos-panel{margin-top:16px;padding:22px;border-radius:17px;color:white;
          background:radial-gradient(circle at 82% 12%,rgba(255,112,184,.14),transparent 35%),
          radial-gradient(circle at 15% 85%,rgba(54,174,245,.16),transparent 35%),linear-gradient(145deg,#07131d,#111d28);
          border:1px solid #2f4b5d}
        .emos-kicker{color:#63bdf4;font-size:.78rem;font-weight:900;letter-spacing:.12em}
        .emos-title{margin-top:.35rem;font-size:clamp(1.45rem,5vw,2rem);font-weight:950}
        .emos-copy{margin-top:.55rem;color:#a8bac7;line-height:1.45}
        .emos-status{display:inline-block;margin-top:13px;padding:5px 10px;border-radius:999px;background:rgba(70,211,155,.12);color:#63d39b;font-weight:900;font-size:.75rem}
        </style>
        <div class="emos-panel">
          <div class="emos-kicker">INSTRUMENT EXPERIMENTAL • E.M.O.S.</div>
          <div class="emos-title">🛰 Scanează starea actuală a Alexandrei</div>
          <div class="emos-copy">Sistem orbital de monitorizare emoțională, bazat pe sateliți imaginari și o încredere complet nejustificată.</div>
          <div class="emos-status">● SISTEM ONLINE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(title: str, text: str, score: int | None) -> None:
    value = f"{score}%" if score is not None else "???"
    caption = "NIVEL EMOȚIONAL ESTIMAT" if score is not None else "VALOARE INDISPONIBILĂ"
    st.markdown(
        f"""
        <style>
        .emos-result{{margin-top:14px;padding:22px;border-radius:16px;text-align:center;color:white;background:linear-gradient(145deg,#0b1722,#152636);border:1px solid #35566b}}
        .emos-result-label{{color:#63bdf4;font-size:.75rem;font-weight:900;letter-spacing:.12em}}
        .emos-result-title{{margin-top:.45rem;font-size:clamp(1.4rem,5vw,2rem);font-weight:950;color:#ffd98d}}
        .emos-result-score{{margin-top:.75rem;font-size:clamp(3rem,12vw,4.8rem);line-height:1;font-weight:950;color:#ff82bf}}
        .emos-result-caption{{color:#96aab8;font-size:.72rem;letter-spacing:.08em;margin-top:.25rem}}
        .emos-result-text{{margin:1rem auto 0;max-width:760px;font-size:1.08rem;line-height:1.55;font-weight:750}}
        .emos-result-foot{{margin-top:1rem;color:#7f95a4;font-size:.75rem}}
        </style>
        <div class="emos-result">
          <div class="emos-result-label">REZULTAT SCANARE</div>
          <div class="emos-result-title">{title}</div>
          <div class="emos-result-score">{value}</div>
          <div class="emos-result-caption">{caption}</div>
          <div class="emos-result-text">{text}</div>
          <div class="emos-result-foot">S.A.T.A. este foarte încrezător. Rareori sigur.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
