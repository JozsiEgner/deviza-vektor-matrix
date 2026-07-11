# Nyílt felhívás / Call for Contributors

## Magyar

Nyilvánosan elindítom a **Deviza‑Vektor Mátrix** nevű nyílt fejlesztési kezdeményezést.

A cél egy auditálható és újrafelhasználható döntéstámogató modul létrehozása, amely az EUR, RUB, CNY és XAU jellegű adatoknál összehasonlítja a súlyozott fundamentális vektorokat a tényleges piaci mozgással.

A referencia-modell kimenetei:

- súlyozott fundamentális pontszám;
- fundamentális–piaci divergenciaszög;
- számított tranzit- vagy megállási idő, ahol az idő kimenet;
- anomáliapontszám;
- `ALLOW`, `REVIEW` vagy `BLOCK` döntési állapot;
- minden döntéshez auditálható indokolás.

A rendszer nem állítja, hogy minden eltérés bizonyított piaci manipuláció. Mérhető anomáliát, inkonzisztens irányt és rendellenes sebességet jelez, amely további tesztet vagy emberi felülvizsgálatot igényel.

### Közreműködőket keresek

- Python- és Rust-fejlesztőket;
- kvantitatív pénzügyi szakembereket;
- pénzügyi modell-ellenőrzőket;
- piaciadat- és API-integrációs fejlesztőket;
- backtesztelési és kockázatkezelési szakértőket;
- nyílt forráskódú projektfenntartókat;
- műszaki dokumentációs és tesztelési közreműködőket.

### Minimális mérnöki követelmények

Éles integráció előtt szükséges:

- backteszt és benchmark-adatkészlet;
- konfigurálható küszöbértékek;
- fals pozitív arány mérése;
- modell- és adatforrás-verziózás;
- auditnapló;
- shadow mód az automatikus blokkolás előtt;
- emberi felülvizsgálati és fail-safe út.

A cél nem garantált kereskedési stratégia közzététele, hanem ellenőrizhető, tesztelhető és továbbfejleszthető anomáliaészlelési és döntéstámogató réteg létrehozása.

— **Égner József Antal**

---

## English

I am opening the **Deviza‑Vektor Mátrix** initiative for public collaboration.

The goal is to build an auditable and reusable decision-support module that compares weighted fundamental vectors with observed market movement for EUR, RUB, CNY and XAU-related data.

The reference model produces:

- a weighted fundamental score;
- a market-versus-fundamental divergence angle;
- a calculated transit or stopping-time estimate where time is an output;
- an anomaly score;
- `ALLOW`, `REVIEW` or `BLOCK` decision states;
- an auditable explanation of every decision.

The system does not claim that every divergence proves market manipulation. It identifies measurable anomalies, inconsistent movement and abnormal speed that require further testing or human review.

Contributors wanted: Python and Rust developers, quantitative finance specialists, model reviewers, market-data/API developers, backtesting and risk-management specialists, maintainers, technical writers and test engineers.

— **Égner József Antal**
