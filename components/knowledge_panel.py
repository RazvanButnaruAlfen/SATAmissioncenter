from datetime import date
import streamlit as st
from core.mission_state import MissionState

KNOWN = [
    ("Prima conexiune", "Martie 2026"),
    ("Distanță inițială", "1984 km"),
    ("Timp petrecut împreună", "Prea puțin"),
    ("Conexiune", "Confirmată în ciuda distanței"),
]
UNKNOWN = [
    "Cum va decurge fiecare zi.",
    "Care va fi cea mai frumoasă amintire.",
    "De câte ori se va schimba planul.",
    "Ce moment va conta cel mai mult.",
]
QUOTES = {
    date(2026, 8, 9): "Distanța fizică a început, în sfârșit, să scadă.",
    date(2026, 8, 12): "Traseul devine mai scurt. Emoțiile refuză să urmeze aceeași logică.",
    date(2026, 8, 13): "Ultima staționare înainte de Ploiești. Nerăbdarea este în creștere.",
    date(2026, 8, 14): "Aproape 2000 km au fost reduși la câțiva pași.",
    date(2026, 8, 15): "Brașovul nu este un test. Este doar o ocazie de a crea amintiri.",
}
DEFAULT = [
    "Uneori este suficient să fiți împreună.",
    "Nu toate lucrurile importante pot fi măsurate în kilometri.",
    "Distanța poate fi calculată. Conexiunea, mai puțin.",
    "S.A.T.A. poate urmări traseul. Restul trebuie trăit.",
]

def render_knowledge_panel(state: MissionState) -> None:
    known_html = "".join(
        f"<div class='k-item'><b>✓ {a}</b><br><span>{b}</span></div>"
        for a, b in KNOWN
    )
    unknown_html = "".join(
        f"<div class='k-item'><b>? </b><span>{x}</span></div>"
        for x in UNKNOWN
    )
    quote = QUOTES.get(state.current_date, DEFAULT[state.current_date.toordinal() % len(DEFAULT)])

    st.markdown(f"""
    <style>
    .k-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}}
    .k-card{{background:#0b1722;border:1px solid #294454;border-radius:16px;padding:20px;color:white}}
    .k-title{{font-size:.8rem;font-weight:900;letter-spacing:.12em;color:#55b9ff;margin-bottom:14px}}
    .k-title.pink{{color:#ff82bf}}
    .k-item{{padding:10px 0;border-bottom:1px solid rgba(115,145,165,.15);line-height:1.4}}
    .k-item:last-child{{border-bottom:none}}
    .k-item span{{color:#dce5eb}}
    .k-quote{{margin-top:14px;padding:22px;border-radius:16px;background:linear-gradient(135deg,#0c1b28,#13293a);
              border:1px solid #2c4b60;text-align:center;color:white}}
    .k-quote div:first-child{{font-size:1.3rem;line-height:1.5;font-weight:800}}
    .k-quote div:last-child{{color:#7fc7f4;margin-top:8px;font-size:.85rem;letter-spacing:.08em}}
    @media(max-width:800px){{.k-grid{{grid-template-columns:1fr}}}}
    </style>
    <div class="k-grid">
      <div class="k-card"><div class="k-title">CE ȘTIE S.A.T.A.</div>{known_html}</div>
      <div class="k-card"><div class="k-title pink">CE NU ȘTIE S.A.T.A.</div>{unknown_html}
      <div style="margin-top:12px;color:#ffd98d;font-weight:800">Din fericire, nu toate lucrurile merită prezise.</div></div>
    </div>
    <div class="k-quote"><div>“{quote}”</div><div>— S.A.T.A.</div></div>
    """, unsafe_allow_html=True)
