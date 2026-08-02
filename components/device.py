from __future__ import annotations

from dataclasses import dataclass

import streamlit as st
from streamlit_js_eval import streamlit_js_eval


MOBILE_BREAKPOINT = 768


@dataclass(frozen=True)
class DeviceInfo:
    width: int | None
    is_mobile: bool
    layout_name: str


def detect_device() -> DeviceInfo:
    """Read the browser viewport width once per Streamlit rerun.

    The JavaScript component must be called at top level, not inside
    an if/else branch. On its first render it may temporarily return
    None; in that case we safely use the desktop layout.
    """
    width = streamlit_js_eval(
        js_expressions="window.innerWidth",
        want_output=True,
        key="SATA_VIEWPORT_WIDTH",
    )

    try:
        normalized_width = int(width) if width is not None else None
    except (TypeError, ValueError):
        normalized_width = None

    detected_mobile = (
        normalized_width is not None
        and normalized_width < MOBILE_BREAKPOINT
    )

    with st.sidebar:
        st.divider()
        st.caption("Responsive development controls")
        override = st.selectbox(
            "Layout preview",
            options=["Automat", "Desktop", "Telefon"],
            index=0,
            help=(
                "Automat folosește lățimea reală a browserului. "
                "Opțiunile Desktop și Telefon sunt utile pentru testare."
            ),
        )

        if override == "Telefon":
            is_mobile = True
        elif override == "Desktop":
            is_mobile = False
        else:
            is_mobile = detected_mobile

        if normalized_width is None:
            st.caption("Lățime browser: în curs de detectare")
        else:
            st.caption(f"Lățime browser detectată: {normalized_width}px")

        st.caption(
            "Layout activ: "
            + ("Telefon" if is_mobile else "Desktop")
        )

    return DeviceInfo(
        width=normalized_width,
        is_mobile=is_mobile,
        layout_name="mobile" if is_mobile else "desktop",
    )
