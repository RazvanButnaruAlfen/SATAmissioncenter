from __future__ import annotations

from dataclasses import dataclass
import random

from .config import MIN_LONGING_FOR_ACCESS, RANDOM_UNLOCK_PROBABILITY
from core.sata_memory import combined_longing_score, has_completed_emos_scan


@dataclass(frozen=True)
class AccessDecision:
    granted: bool
    score: int | None
    reason: str


def check_access(score: int | None, rng: random.Random) -> AccessDecision:
    # During migration, callers may still supply the legacy E.M.O.S. score.
    # The shared memory result takes precedence because it can include
    # Fricometru data as well.
    shared_score = combined_longing_score()
    if shared_score is not None:
        score = shared_score

    if not has_completed_emos_scan():
        return AccessDecision(
            False,
            None,
            "Nu există încă o scanare E.M.O.S. în memoria sistemului.",
        )

    if score is None:
        return AccessDecision(
            False,
            None,
            "Scanarea E.M.O.S. a fost recepționată, dar coeficientul numeric este temporar indisponibil.",
        )
    if score >= MIN_LONGING_FOR_ACCESS and rng.random() < RANDOM_UNLOCK_PROBABILITY:
        return AccessDecision(True, score, "Coeficientul emoțional a depășit accidental toate barierele de securitate.")
    if score < MIN_LONGING_FOR_ACCESS:
        return AccessDecision(False, score, "Dorul estimat nu este la nivelul corespunzător pentru acces.")
    return AccessDecision(False, score, "Nivelul este suficient, dar S.A.T.A. nu se simte încă pregătit să dezvăluie informația.")
