from __future__ import annotations

from datetime import date
import random

from .database import load_packets
from .packet_types import RecoveredPacket
from .storage import (
    increment_actions,
    pending_packet,
    reset_actions,
    seen_ids,
    set_pending,
)


def register_action(
    *,
    today: date,
    trigger: str,
    rng: random.Random | None = None,
    force_drop: bool = False,
) -> RecoveredPacket | None:
    existing = pending_packet(today)
    if existing is not None:
        return existing

    attempts = increment_actions(today)
    random_source = rng or random.SystemRandom()

    # Invisible soft-pity system: the chance grows after every action.
    probability = min(0.74, 0.045 + max(0, attempts - 1) * 0.07)
    should_drop = (
        force_drop
        or attempts >= 10
        or random_source.random() < probability
    )

    if not should_drop:
        return None

    packets = list(load_packets())
    already_seen = seen_ids(today)
    available = [packet for packet in packets if packet.id not in already_seen]

    if not available:
        available = packets

    packet = random_source.choice(available)
    set_pending(today, packet, trigger=trigger)
    reset_actions(today)
    return packet
