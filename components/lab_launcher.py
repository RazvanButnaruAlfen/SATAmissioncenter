import streamlit as st

def render_lab_launcher() -> None:
    st.markdown("""
    <style>
    .lab-shell{margin-top:16px;padding:20px;border-radius:16px;background:linear-gradient(135deg,#17101d,#21152a);
               border:1px solid #5b365f;color:white}
    .lab-title{color:#ff82bf;font-size:.8rem;font-weight:900;letter-spacing:.12em}
    .lab-grid{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:12px;margin-top:14px}
    .lab-card{background:#110d15;border:1px solid #47304d;border-radius:14px;padding:16px;min-height:110px}
    .lab-name{font-size:1.1rem;font-weight:900;color:#ff9bc9}
    .lab-status{margin-top:9px;color:#9fb1bf;line-height:1.4}
    .ok{color:#63d39b;font-weight:900}.soon{color:#f2b84b;font-weight:900}
    @media(max-width:800px){.lab-grid{grid-template-columns:1fr}}
    </style>
    <div class="lab-shell">
      <div class="lab-title">LABORATOR S.A.T.A. • INSTRUMENTE EXPERIMENTALE</div>
      <div class="lab-grid">
        <div class="lab-card"><div class="lab-name">📈 FRICOMETRU.EXE</div>
        <div class="lab-status">Status: <span class="ok">OPERAȚIONAL</span><br>Acuratețe imposibil de demonstrat.</div></div>
        <div class="lab-card"><div class="lab-name">🧪 SIMULATOR PANICĂ</div>
        <div class="lab-status">Status: <span class="soon">ÎN DEZVOLTARE</span></div></div>
        <div class="lab-card"><div class="lab-name">🔍 DETECTOR NEGARE</div>
        <div class="lab-status">Status: <span class="soon">NECESITĂ CALIBRARE</span></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/fricometru.py", label="📈 Deschide FRICOMETRU.EXE", icon="🧪", use_container_width=True)
