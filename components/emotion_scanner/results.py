from datetime import date
import random


EUROPE_RESULTS = [
    ("CALM SUSPECT", "Alexandra pare liniștită. Sistemul consideră această informație insuficient de credibilă.", 38),
    ("NERĂBDARE BINE CAMUFLATĂ", "Nu s-a detectat panică. S-au detectat însă prea multe gânduri despre august pentru a fi o coincidență.", 52),
    ("MONITORIZARE ACTIVĂ", "Calendarul este verificat mental mai des decât ar recunoaște operatorul analizat.", 46),
]

ROMANIA_RESULTS = [
    ("PRECIZIE CRESCUTĂ", "Răzvan se află în aceeași țară. România a devenit brusc prea mică pentru confortul algoritmilor.", 68),
    ("APROPIERE DETECTATĂ", "Distanța s-a redus. Numărul scenariilor posibile a refuzat să coopereze.", 74),
    ("CALM DECLARAT", "Alexandra afirmă că situația este sub control. Declarația a fost arhivată la «optimism suspect».", 65),
]

PLOIESTI_RESULTS = [
    ("CONTACT APROPIAT", "Distanța operațională este zero. Algoritmii au devenit vizibil mai puțin siguri pe ei.", 87),
    ("ZÂMBETE DETECTATE", "Probabilitatea de tachinare este ridicată. Probabilitatea de plictiseală este neglijabilă.", 83),
    ("ANALIZĂ INSTABILĂ", "Alexandra este prea aproape pentru o analiză obiectivă. Se recomandă observație directă.", 91),
]

BRASOV_RESULTS = [
    ("MODELE DEPĂȘITE", "Realitatea a refuzat să respecte simulările. S.A.T.A. recomandă continuarea weekendului.", 96),
    ("PROTOCOL CARPAȚI", "S-au detectat emoții, glume și posibilitatea unor amintiri foarte bune.", 93),
    ("STARE NECALCULABILĂ", "Toate modelele au cedat. Anomalia este considerată pozitivă.", 98),
]

RARE_RESULTS = [
    ("EROARE 418", "Alexandra a observat că este scanată. Retragere tactică recomandată.", None),
    ("ACCES LIMITAT", "Starea actuală este clasificată. Nici S.A.T.A. nu știe exact de ce.", None),
    ("ANOMALIE", "Scannerul a detectat o glumă înainte ca aceasta să fie spusă.", None),
    ("PAUZĂ TEHNICĂ", "Algoritmul a solicitat cafea înainte de a continua analiza.", None),
]


def pool_for_day(current_date: date):
    if date(2026, 8, 15) <= current_date <= date(2026, 8, 17):
        return BRASOV_RESULTS
    if current_date >= date(2026, 8, 14):
        return PLOIESTI_RESULTS
    if current_date >= date(2026, 8, 9):
        return ROMANIA_RESULTS
    return EUROPE_RESULTS


def choose_result(current_date: date, rng: random.Random, rare_probability: float):
    if rng.random() < rare_probability:
        return rng.choice(RARE_RESULTS)
    return rng.choice(pool_for_day(current_date))
