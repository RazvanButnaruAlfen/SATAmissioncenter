# Changelog

## 0.4.0 — Recovered Packets v1
- Modularizat complet subsistemul Recovered Packets.
- Adăugate bancuri, fun facts, rețete, filme și mini-antrenamente.
- Fiecare categorie este păstrată într-un fișier JSON separat.
- Adăugat sistem invizibil de probabilitate cu șansă crescătoare.
- Surpriza este garantată după suficiente interacțiuni, fără afișarea regulii.
- Pachetele nu se repetă în aceeași zi până la epuizarea listei.
- Adăugată animație de decriptare.
- Adăugată arhivă locală a pachetelor recuperate în sesiune.

# Changelog

## 0.3.6 RC3 — Dynamic Scan Results
- Recomandarea Dosarelor Clasificate este acum contextuală.
- După o scanare, sistemul confirmă explicit că datele E.M.O.S. au fost recepționate.
- Pragul și diferența până la acces sunt afișate clar.
- O nouă scanare nu mai este prezentată ca obligatorie.
- Fiecare profil E.M.O.S. folosește o plajă de scoruri, nu o valoare fixă.
- Rezultatul imediat anterior este exclus din selecția următoare.
- Adăugate profiluri și observații noi pentru variație.

# Changelog

## 0.3.5 RC2 — E.M.O.S. Memory Fix
- Separată existența scanării de existența unui scor numeric.
- Rezultatele rare cu scor «???» sunt recunoscute drept scanări finalizate.
- Pentru scanări neconcludente, S.A.T.A. folosește temporar un coeficient operațional de 58%.
- Dosarele Clasificate nu mai cer repetarea scanării după ce E.M.O.S. a rulat.
- Refuzurile vechi de tip «scanare necesară» sunt eliminate automat.
- Adăugată compatibilitate cu valorile legacy din session_state.

# Changelog

## 0.3.4 RC1 — Playable Release Candidate
- Adăugat sistemul invizibil Recovered Packets.
- Pachetele pot conține bancuri, fun facts, rețete, filme sau exerciții.
- Șansa de interceptare crește discret după interacțiuni nereușite.
- După suficiente interacțiuni, sistemul garantează o surpriză fără a dezvălui regula.
- Pachetele nu se repetă în aceeași zi până la epuizarea listei.
- Adăugat flux de decriptare manuală.
- Activat modul Release: fără Development Build și controale responsive vizibile.

# Changelog

## 0.3.3 — Connected Systems
- Adăugată memoria operațională comună S.A.T.A.
- E.M.O.S. salvează scanarea în memoria comună.
- Fricometrul transmite scorul și predicția către S.A.T.A.
- Dosarele Clasificate folosesc un coeficient combinat E.M.O.S. + Fricometru.
- Încercările și documentele deblocate sunt memorate central.
- Adăugat panoul de sincronizare dintre instrumente.
- Laboratorul afișează instrumentele conectate.

# Changelog

## 0.3.2
- Rebuilt E.M.O.S. overlay as compact, single-line HTML.
- Removed all Markdown-sensitive indentation and blank lines.
- Fixed raw HTML fragments appearing during scan progress below 58%.
- Added progress clamping, escaped text, and smoother bar transitions.

## 0.3.0 Foundation Build
- E.M.O.S. migrated from a single file to a modular package.
- Added fullscreen blue pulse, pink target-acquired pulse, scan line and staged scan sequence.
- E.M.O.S. stores the latest score in shared session state.
- Added modular Classified Archives subsystem.
- Archives read the latest E.M.O.S. result and usually deny access for absurdly professional reasons.
- Added shared S.A.T.A. personality rules.
