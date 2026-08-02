import streamlit as st

from core.app_config import APP_VERSION, RELEASE_MODE


def render_footer() -> None:
    st.divider()

    if RELEASE_MODE:
        st.caption(
            "S.A.T.A. Mission Center • Semnal securizat • "
            "Conexiune operațională"
        )
    else:
        st.caption(
            f"S.A.T.A. Mission Center — Development Build {APP_VERSION}"
        )
