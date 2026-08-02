from __future__ import annotations

from datetime import date
import random


EUROPE_RESULTS = [
    {
        "title": "CALM SUSPECT",
        "text": "Alexandra pare liniștită. Sistemul consideră această informație insuficient de credibilă.",
        "score_range": (34, 44),
    },
    {
        "title": "NERĂBDARE BINE CAMUFLATĂ",
        "text": "Nu s-a detectat panică. S-au detectat însă prea multe gânduri despre august pentru a fi o coincidență.",
        "score_range": (46, 58),
    },
    {
        "title": "MONITORIZARE ACTIVĂ",
        "text": "Calendarul este verificat mental mai des decât ar recunoaște operatorul analizat.",
        "score_range": (41, 53),
    },
    {
        "title": "CURIOSITATE CONTROLATĂ",
        "text": "Subiectul pare calm, dar algoritmul a detectat o atenție neobișnuită acordată apropierii misiunii.",
        "score_range": (39, 55),
    },
]

ROMANIA_RESULTS = [
    {
        "title": "PRECIZIE CRESCUTĂ",
        "text": "Răzvan se află în aceeași țară. România a devenit brusc prea mică pentru confortul algoritmilor.",
        "score_range": (62, 72),
    },
    {
        "title": "APROPIERE DETECTATĂ",
        "text": "Distanța s-a redus. Numărul scenariilor posibile a refuzat să coopereze.",
        "score_range": (68, 79),
    },
    {
        "title": "CALM DECLARAT",
        "text": "Alexandra afirmă că situația este sub control. Declarația a fost arhivată la «optimism suspect».",
        "score_range": (59, 71),
    },
    {
        "title": "SEMNAL EMOȚIONAL STABIL",
        "text": "Datele sunt coerente. S.A.T.A. găsește acest lucru neașteptat și va continua verificările.",
        "score_range": (64, 77),
    },
]

PLOIESTI_RESULTS = [
    {
        "title": "CONTACT APROPIAT",
        "text": "Distanța operațională este zero. Algoritmii au devenit vizibil mai puțin siguri pe ei.",
        "score_range": (82, 92),
    },
    {
        "title": "ZÂMBETE DETECTATE",
        "text": "Probabilitatea de tachinare este ridicată. Probabilitatea de plictiseală este neglijabilă.",
        "score_range": (78, 89),
    },
    {
        "title": "ANALIZĂ INSTABILĂ",
        "text": "Alexandra este prea aproape pentru o analiză obiectivă. Se recomandă observație directă.",
        "score_range": (86, 95),
    },
    {
        "title": "INTERACȚIUNE CONFIRMATĂ",
        "text": "Semnalul este puternic. Scannerul refuză să precizeze dacă acest lucru îl ajută sau îl încurcă.",
        "score_range": (80, 93),
    },
]

BRASOV_RESULTS = [
    {
        "title": "MODELE DEPĂȘITE",
        "text": "Realitatea a refuzat să respecte simulările. S.A.T.A. recomandă continuarea weekendului.",
        "score_range": (91, 99),
    },
    {
        "title": "PROTOCOL CARPAȚI",
        "text": "S-au detectat emoții, glume și posibilitatea unor amintiri foarte bune.",
        "score_range": (88, 97),
    },
    {
        "title": "STARE NECALCULABILĂ",
        "text": "Toate modelele au cedat. Anomalia este considerată pozitivă.",
        "score_range": (93, 100),
    },
    {
        "title": "SEMNALE POZITIVE MULTIPLE",
        "text": "Sistemul a detectat prea multe variabile bune și a renunțat temporar la prudență.",
        "score_range": (90, 99),
    },
]

RARE_RESULTS = [
    ("EROARE 418", "Alexandra a observat că este scanată. Retragere tactică recomandată.", None),
    ("ACCES LIMITAT", "Starea actuală este clasificată. Nici S.A.T.A. nu știe exact de ce.", None),
    ("ANOMALIE", "Scannerul a detectat o glumă înainte ca aceasta să fie spusă.", None),
    ("PAUZĂ TEHNICĂ", "Algoritmul a solicitat cafea înainte de a continua analiza.", None),
]

OBSERVATIONS = [
    "Marja de eroare rămâne clasificată.",
    "S.A.T.A. recomandă să nu se tragă concluzii pripite, apoi trage una oricum.",
    "Rezultatul diferă ușor de scanarea precedentă. Sistemul consideră acest lucru foarte științific.",
    "Semnalul a fluctuat în limite considerate convenabile de algoritm.",
    "Precizia estimată este ridicată. Precizia reală nu a fost invitată la ședință.",
]


def pool_for_day(current_date: date):
    if date(2026, 8, 15) <= current_date <= date(2026, 8, 17):
        return BRASOV_RESULTS
    if current_date >= date(2026, 8, 14):
        return PLOIESTI_RESULTS
    if current_date >= date(2026, 8, 9):
        return ROMANIA_RESULTS
    return EUROPE_RESULTS


def choose_result(
    current_date: date,
    rng: random.Random,
    rare_probability: float,
    previous_title: str | None = None,
):
    if rng.random() < rare_probability:
        rare = [item for item in RARE_RESULTS if item[0] != previous_title] or RARE_RESULTS
        return rng.choice(rare)

    pool = pool_for_day(current_date)
    candidates = [item for item in pool if item["title"] != previous_title] or pool
    profile = rng.choice(candidates)
    low, high = profile["score_range"]
    score = rng.randint(low, high)
    text = f'{profile["text"]} {rng.choice(OBSERVATIONS)}'
    return profile["title"], text, score
