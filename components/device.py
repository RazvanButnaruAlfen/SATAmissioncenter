from __future__ import annotations

from dataclasses import dataclass

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from core.app_config import SHOW_RESPONSIVE_DEBUG


MOBILE_BREAKPOINT = 768


@dataclass(frozen=True)
class DeviceInfo:
    width: int | None
    is_mobile: bool
    layout_name: str


def detect_device() -> DeviceInfo:
    width = streamlit_js_eval(
        js_expressions="window.innerWidth",
        want_output=True,
        key="SATA_VIEWPORT_WIDTH",
    )

    try:
        normalized_width = int(width) if width is not None else None
    except (TypeError, ValueError):
        normalized_width = None

    is_mobile = (
        normalized_width is not None
        and normalized_width < MOBILE_BREAKPOINT
    )

    if SHOW_RESPONSIVE_DEBUG:
        with st.sidebar:
            st.divider()
            st.caption("Responsive development controls")
            override = st.selectbox(
                "Layout preview",
                options=["Automat", "Desktop", "Telefon"],
                index=0,
            )

            if override == "Telefon":
                is_mobile = True
            elif override == "Desktop":
                is_mobile = False

            st.caption(
                "Lățime browser: "
                + (
                    "în curs de detectare"
                    if normalized_width is None
                    else f"{normalized_width}px"
                )
            )
            st.caption(
                "Layout activ: "
                + ("Telefon" if is_mobile else "Desktop")
            )

    return DeviceInfo(
        width=normalized_width,
        is_mobile=is_mobile,
        layout_name="mobile" if is_mobile else "desktop",
    )
