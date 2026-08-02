import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <style>
        .archive-shell{margin-top:16px;padding:22px;border-radius:17px;color:white;background:linear-gradient(145deg,#171018,#241524);border:1px solid #67405a}
        .archive-kicker{color:#ff82bf;font-size:.78rem;font-weight:900;letter-spacing:.12em}
        .archive-title{margin-top:.4rem;font-size:clamp(1.45rem,5vw,2rem);font-weight:950}
        .archive-copy{margin-top:.55rem;color:#c2afbd;line-height:1.45}
        </style>
        <div class="archive-shell">
          <div class="archive-kicker">S.A.T.A. • DOSARE CLASIFICATE</div>
          <div class="archive-title">🔒 Dosare clasificate</div>
          <div class="archive-copy">Accesul este protejat prin standarde emoționale pe care sistemul le modifică atunci când este convenabil.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_denied(reason: str, score: int | None, recommendation: str) -> None:
    score_text = "NEDETERMINAT" if score is None else f"{score}%"
    st.error("ACCES REFUZAT")
    st.markdown(f"**Motiv:** {reason}")
    st.markdown(f"**Nivel de dor înregistrat:** `{score_text}`")
    st.info(recommendation)


def render_document(document: dict) -> None:
    st.success("ACCES ACORDAT — EVENIMENT EXTREM DE RAR")
    st.markdown(f"### {document['id']} — {document['title']}")
    st.write(document["text"])
