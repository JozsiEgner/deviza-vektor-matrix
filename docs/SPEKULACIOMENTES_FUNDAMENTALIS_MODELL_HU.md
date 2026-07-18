# Spekulációmentes fundamentális piacmodell

## 1. Kiindulási alapelv

A pénzügyi piacokon alkalmazott képletek többsége közelítés, mert a piac nem zárt fizikai rendszer, hanem komplex, adaptív hálózat.

A projekt célja nem a hagyományos technikai elemzés továbbépítése, hanem egy olyan auditálható döntéstámogató réteg létrehozása, amely valós gazdasági és fizikai változókat használ:

- kamatok és kötvényhozamok;
- spot- és határidős árak;
- tárolási, biztosítási és logisztikai költségek;
- fizikai készletadatok;
- kereskedelmi mérlegek;
- finanszírozási és likviditási mutatók;
- devizánkénti kockázati és intervenciós változók.

A modell szakmai alapja az arbitrázsmentes árazás és a Cost-of-Carry összefüggés.

> A rendszer nem bizonyít manipulációt, nem garantál jövőbeli irányt, és nem helyettesíti a backtesztet vagy az emberi felülvizsgálatot. Mérhető anomáliát, divergenciát és modellinkonzisztenciát jelez.

---

## 2. Cost-of-Carry modell

Az arbitrázsmentes határidős ár:

\[
F_T=S_0\cdot e^{(r+u-y)T}
\]

ahol:

- \(S_0\): jelenlegi spot ár;
- \(F_T\): határidős ár;
- \(r\): kockázatmentes kamatláb;
- \(u\): tárolási és tartási költség;
- \(y\): convenience yield;
- \(T\): lejáratig hátralévő idő.

A nettó drift:

\[
NetDrift=r+u-y
\]

Az implicit idő:

\[
t_{calc}=\frac{\ln(F_T/S_0)}{r+u-y}
\]

Ez az érték nem automatikusan a piac „hátralévő ideje”, hanem az az implicit időhorizont, amely mellett a megfigyelt spot és futures ár összhangban lenne a megadott Cost-of-Carry paraméterekkel.

---

## 3. Fundamentális mátrix

A minimális bemeneti vektor:

\[
\vec{x}=
\begin{bmatrix}
S_0\\
F_T\\
r\\
u\\
y
\end{bmatrix}
\]

Több instrumentum vagy lejárat esetén:

\[
X=
\begin{bmatrix}
S_{0,1} & F_1 & r_1 & u_1 & y_1\\
S_{0,2} & F_2 & r_2 & u_2 & y_2\\
\vdots & \vdots & \vdots & \vdots & \vdots\\
S_{0,n} & F_n & r_n & u_n & y_n
\end{bmatrix}
\]

| Tényező | Jelölés | Példaforrás | Szerep |
|---|---:|---|---|
| Spot ár | \(S_0\) | XAU/USD pillanatnyi ár | Kiindulási érték |
| Határidős ár | \(F_T\) | COMEX/CME futures | Piaci célérték |
| Kockázatmentes kamat | \(r\) | Állampapír- vagy pénzpiaci hozam | Finanszírozási drift |
| Tárolási költség | \(u\) | Biztosítás, páncélterem, logisztika | Tartási költség |
| Convenience yield | \(y\) | Fizikai készlet- és lease-adatok | Fizikai birtoklási előny |
| Lejárat | \(T\) | Futures-szerződés | Ellenőrzési horizont |
| Implicit idő | \(t_{calc}\) | Modellkimenet | Diagnosztikai érték |

---

## 4. Fair érték és basis

A fair határidős ár:

\[
F_{fair}=S_0\cdot e^{(r+u-y)T}
\]

A basis:

\[
Basis=F_{market}-F_{fair}
\]

Százalékos formában:

\[
Basis_{\%}=\frac{F_{market}-F_{fair}}{F_{fair}}\cdot100
\]

A basis önmagában nem bizonyít manipulációt. A modell feladata annak vizsgálata, hogy az eltérés meghaladja-e a tranzakciós, finanszírozási, szállítási és likviditási költségekkel indokolható tartományt.

---

## 5. Anomália- és divergenciaészlelés

A rendszer kockázati jelzést adhat, ha például:

1. a piaci ár tartósan eltér a fair értéktől;
2. az implicit idő negatív vagy instabil;
3. a számított convenience yield kilép az elfogadható tartományból;
4. a nettó drift közel nulla, miközben jelentős árkülönbség látható;
5. az ár lényegesen gyorsabban változik, mint a fundamentális inputok;
6. a basis nem konvergál a lejárathoz közeledve;
7. a spot és futures piac kapcsolata tartósan szétesik;
8. a fizikai készletadat és a tőzsdei ármozgás ellentétes képet mutat.

A javasolt döntési állapotok:

- `ALLOW`: a piaci és fundamentális állapot összhangban van;
- `REVIEW` vagy `REDUCE`: eltérés látható, további vizsgálat szükséges;
- `BLOCK`: a jel instabil, adatminősége gyenge vagy a modellkimenet fizikailag/gazdaságilag irreális.

---

## 6. Basis convergence

Normál körülmények között a futures árnak lejáratkor a spot árhoz kell közelítenie:

\[
\lim_{T\to0}F_T=S_0
\]

Ha a konvergencia nem következik be, lehetséges okok:

- likviditási hiány;
- szállítási probléma;
- fizikai készlethiány;
- finanszírozási zavar;
- kereskedési korlátozás;
- adatminőségi hiba;
- rendkívüli piaci esemény.

A rendszer ezért ne automatikusan manipulációt állapítson meg, hanem növelje az anomáliapontszámot és kérjen további megerősítést.

---

## 7. Vektorszög és szögsebesség

Legyen \(\vec{E}_{fund}\) a fundamentális erővektor, \(\vec{E}_{market}\) pedig a megfigyelt piaci mozgásvektor.

A két vektor közötti szög:

\[
\theta=\cos^{-1}\left(\frac{\vec{E}_{fund}\cdot\vec{E}_{market}}{\|\vec{E}_{fund}\|\|\vec{E}_{market}\|}\right)
\]

Értelmezési javaslat:

- \(0^\circ\): teljes irányegyezés;
- \(0^\circ-30^\circ\): erős összhang;
- \(30^\circ-60^\circ\): részleges divergencia;
- \(60^\circ-90^\circ\): jelentős eltérés;
- \(90^\circ\): a piaci mozgás merőleges a fundamentális vektorra;
- \(90^\circ-180^\circ\): részben vagy teljesen ellentétes mozgás.

A szögsebesség:

\[
\omega=\frac{\Delta\theta}{\Delta t}
\]

Extrém gyors szögváltozás flash-crash, likviditási vákuum, algoritmikus kereskedési hullám, hibás adat vagy más technikai torzulás jele lehet.

---

## 8. Csúszási sebesség

A piaci és fundamentális állapot közötti távolság változási sebessége:

\[
v_{slip}=\frac{\Delta\|\vec{E}_{market}-\vec{E}_{fund}\|}{\Delta t}
\]

Magas csúszási sebesség esetén a rendszer:

- csökkentheti a bizalmi pontszámot;
- növelheti az anomáliafaktort;
- szigoríthatja a kockázati kaput;
- blokkolhatja az automatikus döntést.

---

## 9. Deviza-Vektor Mátrix

Az EUR, RUB és CNY fundamentális szerkezete:

\[
M=
\begin{bmatrix}
r_{EUR} & CA_{EUR} & RP_{EUR}\\
r_{RUB} & CA_{RUB} & RP_{RUB}\\
r_{CNY} & CA_{CNY} & RP_{CNY}
\end{bmatrix}
\]

ahol:

- \(r_i\): kamat- vagy kamatkülönbözeti komponens;
- \(CA_i\): kereskedelmi vagy folyó fizetési mérleg;
- \(RP_i\): kockázati prémium vagy intervenciós komponens.

| Deviza | Kamatkomponens | Kereskedelmi komponens | Kockázati komponens |
|---|---|---|---|
| EUR | EKB-kamat, hozamgörbe | Eurozóna export- és folyómérleg | Energiafüggés, politikai és hitelkockázat |
| RUB | Jegybanki kamat | Olaj- és gázexport | Szankciók, konvertibilitás, tőkekorlátozások |
| CNY | PBOC referencia és fixing | Kínai kereskedelmi mérleg | Intervenciós sáv, tőkekontroll, fixingeltérés |

Devizánkénti normalizált erővektor:

\[
\vec{E}_i=w_r\hat{r}_i+w_{CA}\widehat{CA}_i-w_{RP}\widehat{RP}_i
\]

Az eredő:

\[
\vec{E}_{FX}=\sum_i\alpha_i\vec{E}_i
\]

---

## 10. XAU és a devizamátrix kapcsolata

Az arany fundamentális vektora például:

\[
\vec{E}_{XAU}=w_1\vec{E}_{USD}+w_2\vec{E}_{real\ rate}+w_3\vec{E}_{liquidity}+w_4\vec{E}_{inventory}+w_5\vec{E}_{risk}
\]

A devizaeredővel való szögkapcsolat:

\[
\theta_{XAU-FX}=\angle(\vec{E}_{XAU},\vec{E}_{FX})
\]

A cél nem egyetlen devizából irányt jósolni, hanem több fundamentális erő együttes állapotát vizsgálni.

---

## 11. Összetett anomáliafaktor

Egy lehetséges normalizált mérőszám:

\[
M_{total}=w_bM_{basis}+w_tM_{time}+w_{\theta}M_{\theta}+w_sM_{slippage}+w_lM_{liquidity}
\]

ahol:

\[
\sum w_i=1
\]

Példaosztályozás:

- 0,00–0,20: normál állapot;
- 0,20–0,40: enyhe eltérés;
- 0,40–0,60: jelentős arbitrázsfeszültség;
- 0,60–0,80: súlyos piaci anomália;
- 0,80–1,00: rendkívüli vagy blokkolandó állapot.

A küszöbértékeket nem szabad univerzális állandónak tekinteni. Backteszttel, benchmark-adatokkal és fals pozitív arány mérésével kell kalibrálni őket.

---

## 12. PowerShell–Python architektúra

Javasolt adatfolyam:

```text
API
  -> PowerShell adatgyűjtő
  -> JSON / CSV
  -> Python / NumPy számítási motor
  -> auditálható eredmény
  -> PowerShell vezérlőréteg
```

A PowerShell feladatai:

- API-hívások;
- adatvalidálás;
- JSON/CSV kezelés;
- folyamatindítás;
- naplózás;
- riasztás és felhasználói felület.

A Python/NumPy feladatai:

- Cost-of-Carry számítás;
- mátrix- és vektorműveletek;
- implicit idő;
- divergenciaszög;
- szögsebesség és csúszási sebesség;
- anomáliapontszám;
- kockázati döntés.

---

## 13. Referencia Python-logika

```python
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionResult:
    decision: str
    reason: str
    net_drift: float
    implied_time_years: float | None
    time_ratio: float | None


def detect_market_anomaly(
    s0: float,
    ft: float,
    r: float,
    u: float,
    y: float,
    actual_time_years: float,
    minimum_drift: float = 1e-8,
    minimum_time_ratio: float = 0.5,
) -> DetectionResult:
    if s0 <= 0 or ft <= 0:
        raise ValueError("A spot és a futures árnak pozitívnak kell lennie.")

    if actual_time_years <= 0:
        raise ValueError("A tényleges időtávnak pozitívnak kell lennie.")

    net_drift = r + u - y

    if abs(net_drift) < minimum_drift:
        return DetectionResult(
            decision="BLOCK",
            reason="A nettó drift közel nulla; az implicit idő instabil.",
            net_drift=net_drift,
            implied_time_years=None,
            time_ratio=None,
        )

    implied_time = math.log(ft / s0) / net_drift

    if implied_time <= 0:
        return DetectionResult(
            decision="BLOCK",
            reason="Negatív vagy nulla implicit idő.",
            net_drift=net_drift,
            implied_time_years=implied_time,
            time_ratio=None,
        )

    time_ratio = actual_time_years / implied_time

    if actual_time_years < minimum_time_ratio * implied_time:
        return DetectionResult(
            decision="REVIEW",
            reason="A mozgás gyorsabb, mint amit a modell indokol.",
            net_drift=net_drift,
            implied_time_years=implied_time,
            time_ratio=time_ratio,
        )

    return DetectionResult(
        decision="ALLOW",
        reason="A mozgás a megadott küszöbökön belül van.",
        net_drift=net_drift,
        implied_time_years=implied_time,
        time_ratio=time_ratio,
    )
```

---

## 14. Közös fejlesztési munkacsomagok

A projekt más fejlesztések összehangolására az alábbi munkacsomagokra bontható:

1. **Adatmodell és séma**
   - egységes JSON Schema;
   - mértékegységek;
   - forrás- és időbélyeg-kezelés.

2. **Cost-of-Carry motor**
   - fair érték;
   - basis;
   - implicit idő;
   - hibakezelés.

3. **Vektor- és mátrixmotor**
   - normalizálás;
   - súlyozás;
   - szög és szögsebesség;
   - csúszási sebesség.

4. **Devizaadapterek**
   - EUR;
   - RUB;
   - CNY;
   - XAU és USD kapcsolat.

5. **Anomáliapontszám és Risk Gate**
   - `ALLOW`;
   - `REVIEW` / `REDUCE`;
   - `BLOCK`;
   - auditálható indoklás.

6. **Backteszt és validáció**
   - benchmark-adatkészlet;
   - fals pozitív arány;
   - érzékenységvizsgálat;
   - küszöbkalibráció.

7. **PowerShell–Python híd**
   - JSON/CSV import;
   - CLI;
   - naplózás;
   - Windows futtatás.

8. **Dokumentáció és governance**
   - verziózott modellleírás;
   - adatforrás-nyilvántartás;
   - közreműködői szabályok;
   - review és release folyamat.

---

## 15. A modell rendeltetése

A projekt célja:

- fair érték meghatározása;
- arbitrázsfeszültség mérése;
- fundamentális és piaci irány összehasonlítása;
- technikai és algoritmikus zaj szűrése;
- rendkívüli eltérések azonosítása;
- auditálható kockázati kapu létrehozása.

A rendszer összefoglaló meghatározása:

> **Fundamentális arbitrázsdetektor, piaci divergenciamérő és auditálható kockázati kapu.**

Projektkezdeményező: **Égner József Antal**
