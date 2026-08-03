from __future__ import annotations

from pathlib import Path

import streamlit.components.v1 as components


_COMPONENT_PATH = Path(__file__).resolve().parent / "frontend"
_frequency_slider = components.declare_component(
    "sata_frequency_slider",
    path=str(_COMPONENT_PATH),
)


def frequency_slider(
    *,
    target: int,
    value: int = 50,
    tolerance: int = 5,
    key: str | None = None,
) -> int:
    result = _frequency_slider(
        target=int(target),
        value=int(value),
        tolerance=int(tolerance),
        key=key,
        default=int(value),
    )
    try:
        return int(result)
    except (TypeError, ValueError):
        return int(value)
