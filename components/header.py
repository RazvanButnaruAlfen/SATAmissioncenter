import streamlit as st

def render_header() -> None:
    st.markdown(
        """
        <style>
        .block-container {max-width:1280px;padding-top:2.2rem;padding-bottom:3rem;}
        .sata-header {
            display:flex;justify-content:space-between;align-items:center;gap:20px;
            padding:22px 28px;border-radius:20px;margin-bottom:18px;
            background:linear-gradient(135deg,#07111a,#132534);
            color:white;border:1px solid #294354;
            box-shadow:0 10px 30px rgba(0,0,0,.13);
        }
        .sata-title {font-size:2.55rem;font-weight:950;letter-spacing:.11em;}
        .sata-subtitle {color:#c5d3dd;font-size:1.02rem;}
        .dev-badge {
            border:2px solid #ff5b5b;color:#ff6868;padding:10px 15px;
            border-radius:10px;font-weight:900;letter-spacing:.08em;
            transform:rotate(-2deg);white-space:nowrap;
        }
        @media(max-width:700px) {
          .sata-header{align-items:flex-start;flex-direction:column;}
          .sata-title{font-size:2rem;}
        }
        </style>
        <header class="sata-header">
          <div>
            <div class="sata-title">📡 S.A.T.A.</div>
            <div class="sata-subtitle">Sistem Automat pentru Tensiunea Alexandrei</div>
            <div style="margin-top:7px;color:#55b9ff;font-weight:800;">
              MISSION CENTER — DEVELOPMENT BUILD 0.2
            </div>
          </div>
          <div class="dev-badge">TOP SECRET • DEV</div>
        </header>
        """,
        unsafe_allow_html=True,
    )
