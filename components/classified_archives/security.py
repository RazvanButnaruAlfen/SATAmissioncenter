from __future__ import annotations

from dataclasses import dataclass
import random

from .config import MIN_LONGING_FOR_ACCESS, RANDOM_UNLOCK_PROBABILITY


@dataclass(frozen=True)
class AccessDecision:
    granted: bool
    score: int | None
    reason: str


def check_access(score: int | None, rng: random.Random) -> AccessDecision:
    if score is None:
        return AccessDecision(False, None, "Nu există o scanare E.M.O.S. validă în memoria sistemului.")
    if score >= MIN_LONGING_FOR_ACCESS and rng.random() < RANDOM_UNLOCK_PROBABILITY:
        return AccessDecision(True, score, "Coeficientul emoțional a depășit accidental toate barierele de securitate.")
    if score < MIN_LONGING_FOR_ACCESS:
        return AccessDecision(False, score, "Dorul estimat nu este la nivelul corespunzător pentru acces.")
    return AccessDecision(False, score, "Nivelul este suficient, dar S.A.T.A. nu se simte încă pregătit să dezvăluie informația.")
