# Deviza‑Vektor Mátrix

Nyílt, auditálható referenciaimplementáció fundamentális és piaci vektorok összehasonlítására EUR, RUB, CNY és XAU jellegű adatoknál.

## Mit csinál?

- súlyozott fundamentális vektort képez;
- összeveti a tényleges piaci mozgással;
- divergenciaszöget számít;
- a célár-távolságból becsült tranzit-/megállási időt ad, ahol az idő kimenet;
- rendellenes gyorsaság és irányeltérés alapján `ALLOW`, `REVIEW` vagy `BLOCK` állapotot ad;
- minden döntéshez auditálható indoklást biztosít.

## Fontos korlát

A modell nem bizonyít piaci manipulációt és nem azonosít szereplőt. Anomáliát, divergenciát és modellinkonzisztenciát jelez. Éles kereskedési vagy fizetési blokkolás előtt backtest, kalibráció, audit és emberi felülvizsgálat szükséges.

## Gyors indítás

```powershell
pip install -e ".[test]"
$env:PYTHONPATH="src"
python -m dvm.cli examples/sample-input.json
pytest
```

PowerShellből:

```powershell
cd powershell
.\run-matrix.ps1
```

## Bemeneti tényezők

A négyes mintavektor szabadon konfigurálható. Például:

1. kamatkülönbözet;
2. folyó mérleg / kereskedelmi mérleg;
3. infláció vagy reálkamat;
4. geopolitikai / intervenciós kockázati proxy.

A tényezőket azonos skálára kell normalizálni, és minden adatponthoz forrásidőbélyeget kell tárolni.

## Közreműködés

Fejlesztőket, kvantitatív szakembereket, pénzügyi modell-ellenőrzőket, adatforrás-integrátorokat és tesztelőket keresünk.

Lásd: [CALL_FOR_CONTRIBUTORS.md](CALL_FOR_CONTRIBUTORS.md)

Projektkezdeményező: **Égner József Antal**
