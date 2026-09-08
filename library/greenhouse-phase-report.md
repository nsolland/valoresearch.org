# Greenhouse — Versjonert fase-rapport

**Versjon:** 1.0.0
**Dato:** 2026-08-06
**Status:** Alle 6 fasar ✅ (POC fullført)
**Repo:** `nsolland/greenhouse` (main, `24de2b8`)

## Samandrag

Agentic Greenhouse POC beviser at laga i Del 4+5 av analyserapporten heng
saman på data — ikkje på papir. Frå grunnmur til rekursiv læring: kvart
lag har eit operasjonalisert exit-kriterium, deterministiske testjiggar og
verifiserte resultat. All kode er stdlib/numpy-basert, utan LLM-avhengigheit
for kjerneprosessane.

| Fase | Innhald | Exit-kriterium | Resultat | Status |
|---|---|---|---|---|
| 0 | Grunnmur & data | Stabil tidsserie + ground truth | TSDB, transform, notat (2 testar) | ✅ |
| 1 | Perception (camera+CSI) | F1 ≥0.8 på ubrukt holdout | acc 0.90, F1 0.92/0.86 | ✅ |
| 2 | RAG-copilot L0→L1 | ≥80 % godkjende svar | 100 % godkjent (6/6 grounded) | ✅ |
| 3 | Autonom L2 A/B | Like yield, mindre energi/vatn/kg, 0 brudd | A: 28.8 kg, 20.0 kWh/kg, 10.1 l/kg | ✅ |
| 4 | World model + twin + sim2real | Sim-trent policy i mini-drivhus; twin A/B-testbar | MAE 0.04, twin 1.0, s2r 1.0 | ✅ |
| 5 | Rekursiv læring + multi-agent | Kjende ukjente + trygg eskalering | MAE 0.082→0.030, 9 eskaleringar | ✅ |

## Detaljerte resultat per fase

### Fase 0 — Grunnmur & data
- `TimeSeriesStore` (in-memory, UTC-timestamping), transform, ground-truth-notat.
- 2 testar grøne.
- Avgrensning: in-memory, ikkje InfluxDB (POC-skjelett).

### Fase 1 — Multi-modalt perceptions-lag
- **Modalitetar:** camera (VLM-embedding, 8-dim), CSI (vatnstress, 4-dim),
  ultralyd, klima.
- `extract_features` → fast 6-dim vektor `[u, humidity, co2, temp, camera_health, csi_stress]`.
- n=800, seed 449527: **accuracy 0.90, holdout F1 0.92 (healthy) / 0.86 (stressed)**,
  `exit_criterion_pass=True`.
- 11 testar grøne. Stabilt på tvers av 5 seeds ved n≥800.
- Bonus-fix: `.gitignore`-regelen `data/` fanga utilsiktet `app/data/synthetic.py` — avgrensa til rot-kun.

### Fase 2 — RAG-chat-copilot L0→L1
- 8 domain-chunks, deterministisk nøkkelord/substreng-retriever (ingen LLM-dep).
- L0 `advice` vs L1 `recommendation`, svar forankra med kjelder.
- **100 % godkjente grounded svar** (6/6), `exit=True`.
- 11 testar grøne.

### Fase 3 — Autonom vann/klima L2
- `PolicyEnforcer` fail-closed: settpunkt utanfor grensa → `PolicyViolation`, aldri utført.
- A/B 30 døgn, deterministisk simulator:

| Arm | Yield | Energi/kg | Vatn/kg | Brudd |
|---|---|---|---|---|
| L2 autonom | **28.8 kg** | **20.0** | **10.1** | 0 |
| Baseline | 18.4 kg | 28.5 | 19.5 | 0 |

- 12 testar grøne. Exit passert.

### Fase 4 — World model + twin + sim2real
- World model: lineær lstsq-prediktor, trent på utforskings-data
  (rike trajektorier), bias-kolonne, fysisk state som input.
- Twin A/B: **coverage 1.0** (300/300 steg innanfor toleranse), MAE state 0.43.
- sim2real: `MiniGreenhouseSim` med fysikk-gap + støy, **yield-retensjon 1.0**, 0 brudd.
- 8 testar grøne.

### Fase 5 — Rekursiv læring + multi-agent
- 4 domene-agentar (klima, energi, helse, logistikk), kvar med dokumenterte kjende ukjente.
- `TrustLadder`: autonomi eskalerer berre på data-bevis (conf ≥0.7) + menneske-godkjenning.
- **Læringssløyfa:** MAE 0.082 → 0.030 → 0.056, `improved_after_loop=True`,
  **9 trygge (menneske-godkjente) eskaleringar**.
- 12 testar grøne.

## Kjende avgrensingar (POC)

- Simulatorar er deterministiske testjiggar, ikkje ekte drivhusfysikk.
- World model er lineær — fangar ikkje sterkt ikkje-lineær dynamikk.
- Agentar er regelbaserte, ikkje LLM.
- Copilot-retrieval er nøkkelords-basert, ikkje ein LLM-embedder.
- Ekte aktuering krev full autoritetskjede (LA3 VAIG → LA4 REHT → LA5 RACS
  → Core → LA6 Veritas) og menneskeleg opsyn.

## Vedlikehald

- Kvar fase har eigen `.venv`, `requirements.txt`, `tests/` og README.
- Fase 4/5 brukar symlinkar til fase-3 (sim/policy/controller) og fase-4 (world) — ingen duplisering.
- All framdrift er commit+push til `main`.
