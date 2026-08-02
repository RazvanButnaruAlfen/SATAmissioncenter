from __future__ import annotations


DENIAL_MESSAGES = [
    "Dorul estimat nu este la nivelul corespunzător pentru acces.",
    "Coeficientul de apropiere nu a atins pragul operațional.",
    "Nivelul de curiozitate compromite obiectivitatea operatorului.",
    "Documentele sunt în curs de reclasificare. Nici noi nu știm de ce.",
    "Autorizația satelitară a expirat exact când devenea interesant.",
]


def recommendation_for_denial(
    *,
    scan_completed: bool,
    score: int | None,
    minimum_score: int,
) -> str:
    if not scan_completed:
        return (
            "Nu există încă date E.M.O.S. Recomandăm Scanarea Emoțională "
            "pentru determinarea nivelului operațional de dor."
        )

    if score is None:
        return (
            "Scanarea E.M.O.S. a fost recepționată, dar rezultatul este "
            "neconcludent. S.A.T.A. a arhivat situația la «mister convenabil»."
        )

    if score < minimum_score:
        difference = minimum_score - score
        return (
            f"Scanarea E.M.O.S. a fost recepționată și înregistrată. Pragul "
            f"de acces este {minimum_score}%, iar valoarea actuală este "
            f"{score}% — cu {difference} puncte sub cerința inventată de sistem. "
            "O nouă scanare este opțională; rezultatele pot fluctua deoarece "
            "S.A.T.A. insistă că emoțiile nu sunt componente calibrate."
        )

    return (
        "Datele E.M.O.S. sunt suficiente. Accesul a fost refuzat dintr-un alt "
        "motiv de securitate, probabil creat în urmă cu câteva secunde."
    )
