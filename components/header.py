import streamlit as st

def render_header() -> None:
    st.markdown(
        '''
        <div style="padding:1.5rem 1.8rem;border-radius:18px;
        background:linear-gradient(135deg,#13212c,#263b4a);
        color:white;margin-bottom:1.2rem;">
          <div style="font-size:2.6rem;font-weight:900;letter-spacing:.08em;">📡 S.A.T.A.</div>
          <div style="font-size:1.15rem;color:#d5e0e8;">
            Sistem Automat pentru Tensiunea Alexandrei
          </div>
          <div style="margin-top:.7rem;font-weight:700;color:#ff6b6b;">
            MISSION CENTER — DEVELOPMENT BUILD
          </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
