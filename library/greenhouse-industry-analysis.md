# Forskning: Drivhusindustrien 2026 — og utkast til et "agentic" drivhus

_Dato: 2026-08-04 · Ekstern research · Kildebasert_

---

## 1. Utfordringer dagens moderne drivhus har

**Energi — den største variable kostnaden**
- Energi (belysning + klima/HVAC) utgjør typisk **30–60 % av omsetningen** i moderne CEA-drivhus
- Høye strøm- og gasspriser presser marginer hardt, spesielt i Europa (vinterdrift, oppvarming)
- Vekslende strømpriser gjør energistyring til et komplekst optimeringsproblem

**Arbeidskraft — mangel på kompetanse**
- **Arbeidskraft = ~40 % av årlige utgifter** for gartnere
- Aldrende gartnerstand, få unge vil inn, sesongarbeid (H-2A-visum) usikkert
- **Kritisk mangel på erfarne "growers"** — ekspertisen finnes ikke lenger i markedet (Blue Radix kaller det "greenhouse aging crisis")

**Teknisk kompleksitet og integrasjon**
- Moderne drivhus består av dusinvis av systemer: varme, ventilasjon, skjerming, vanning, CO2, belysning — som må koordineres som én enhet
- **Mixed-vendor-legacy**: klima-computer fra én leverandør, irrigasjonskontroller fra en annen, sensorer fra flere — middleware og API-kostnader bremser AI-adopsjon

**Andre utfordringer:**
- Klimaendringer/ekstremvær som forstyrrer produksjonen
- Vannknapphet → krav om lukkede hydroponiske systemer
- EU-krav (Farm to Fork: 50 % pesticidreduksjon innen 2030) → dokumentasjon og presisjon
- Høye CapEx-kostnader for klimakontroll-utstyr (Priva One, Ridder Hortimax Pro er dyre)
- **Growers' tillit til AI**: "assisted autonomy" selger bedre enn full hands-off
- Markedet: Greenhouse automation = **$3,2 mrd (2025) → $7,1 mrd (2034)**, 9,8 % CAGR

---

## 2. Kostnads- og inntektsdrivere

### Kostnadsdrivere
| Driver | Størrelse |
|---|---|
| Energi (LED-belysning + HVAC/klima) | 30–60 % av omsetning |
| Arbeidskraft (lønn FTE) | 40 % av årlige utgifter |
| Facility lease/avskrivning | Største faste kostnad |
| Inputs: frø, substrat, næring | 50–60 % av omsetning (COGS) |
| Logistikk/distribusjon | ~40 % av omsetning |
| Forsikring, admin, energi-topper | Fast overhead |

### Inntektsdrivere
- **Utbytte per kvadratmeter** — kjernen i hele økonomien (tomater, agurk, paprika, salat)
- **Året-runt-produksjon** — utvider sesongen og sikrer stabile leveranser
- **Premium-priser**: lokal, fersk, høy kvalitet, konsistens (retail + foodservice-kontrakter med QSR-kjeder)
- **Høyverdi-avlinger**: tomater leder volum; salat/leafy greens raskeste vekst; mikrogrønt/urter til restauranter har best margin per m²
- **Utbyttegevinst vs. felt**: jordbær 40–50 t/ha i drivhus mot 15–20 t/ha felt (2–3×)
- Vertikal farming: 200–500 % utbytteøkning, men mye høyere energi → lønnsomt kun for premium

---

## 3. Digitale verktøy — HW og SW

### Hardware
- **Klima-computere**: Priva Connext/Compass/Compact CC, Hoogendoorn IIVO (iSii utgikk jan 2026), Ridder Hortimax, Argus TITAN 900/Axia
- **Sensorer/IoT**: Aranet, 30MHz, klima-/fukt-/CO2-/lys-sensorer, kameraer
- **LED-belysning**: Signify (Philips GrowWise) — global leder
- **Fertigation/irrigasjon**: Netafim (presisjonsirrigasjon), fertigation-managere
- **Skjermer (screens)**: Ridder leder segmentet
- **Robotikk/høsting**, rolling benches (Logiqs), materialhandling
- **CO2-dosering, CHP/energisystemer, varmepumper**

### Software
- **Kontroll-OS**: Priva One (integrert OS: klima, irrigasjon, energi, prosesser), Priva Connext dataplatform, Open Platform med 60+ integrasjonspartnere
- **Ridder Hortimax Pro** (åpen tilkoblet plattform), **Hoogendoorn IIVO** (autonomt fokus), **Argus LIVE/Axia**
- **AI-overlay-lag** (kjører oppå eksisterende HW): **Blue Radix Crop Controller**, Source.ag Workspace, **IUNU LUNA** (plantenivå-vision), Koidra, GrowDirector 4 PRO
- **Cloud/edge**, SCADA-lignende sentrale dashboards, telemetri, ERP-integrasjon, skyplattformer (Azure IoT hos Blue Radix)
- **Raskest voksende segment: Software/SaaS, 13,6 % CAGR**

---

## 4. Hvem dominerer?

### Hardware
- **Priva B.V. (NL)** — bredest plattform, kunder i 100+ land, "økosystem-orkestrator"
- **Ridder Group (NL)** — leder på skjermsystemer, ekspanderer inn robot-høsting
- **Hoogendoorn (NL)** — 100+ land, satser alt på IIVO/autonomt
- **Argus Controls (Canada)** — Nord-Amerikas leder, forsknings-kvalitet
- **Signify/Philips** — global LED-leder
- **Netafim** — presisjonsirrigasjon

### Software / AI
- **Blue Radix** — markedsleder innen Autonomous Growing (Crop Controller)
- **Source.ag** — AI-overlay, integrert med Priva PIM/Connext
- **Priva One + konkurrentene** — eier den installerte basen som alt AI kobles på

### Mønster
Markedet deler seg i to lag — **inkumbenter** (Priva, Ridder, Hoogendoorn, Argus) som eier HW/utførelse, og **AI-challengere** (Source.ag, Blue Radix, Koidra, IUNU) som bygger intelligenslaget oppå. Top 10 = ~42–48 % av global inntekt. **Nederland er teknologiklyngen**: ~10 000 ha glass, alle store leverandører + Wageningen University (WUR). Europa = 34–42 % av markedet.

---

## 5. Hvordan kan et "agentic" drivhus se ut? — Forslag

Basert på det som finnes i markedet (Blue Radix "digital brain", RAG-grounded LLM-agenter i vitenskapelig litteratur, LLM-behavior-tree-robotikk) foreslås følgende arkitektur:

### Lagdelt multi-agent-arkitektur

1. **Sensing-lag**: IoT-sensorer (temp, fukt, CO2, lys, EC/pH), kameraer, værvarsel, sanntids strømpriser, vannstatus
2. **Persepsjonslag (VLM)**: kamera-AI som leser plantehelse, sykdom, skadedyr, fruktmodning (som IUNU LUNA / CLIP-baserte modeller)
3. **Reasoning-lag — spesialiserte LLM-agenter** (orchestrated av en orkestrator med policy-grenser):
   - **Crop Strategy Agent** — setter vekstplan/mål for hele sesongen
   - **Climate Agent** — beregner optimale setpoints (temp/fukt/CO2/lys) hvert 5. minutt
   - **Energy Agent** — optimaliserer mot strømpriser, buffere, CHP/avjord
   - **Irrigation/Fertigation Agent** — presis vanning/næring
   - **Health Agent** — sykdom/pest-overvåking og tiltak
   - **Logistics/Labor Agent** — høstings-/pakkeplanlegging
4. **Aktueringslag**: sender setpoints direkte til eksisterende klimakomputer via API (Priva/Ridder/Argus) — **ingen HW-utskifting**, AI lagt oppå
5. **Safety/Governance**: menneskelig opsyn ("Autonomous Greenhouse Manager" på avstand), policy-gjerder, full logging, exception-håndtering

### Gradert autonomi (trinn)
- **L0:** AI gir råd → dyrker godkjenner
- **L1:** Auto-anbefalinger med godkjenningsflyt
- **L2:** Autonom styring innenfor definerte grenser (Blue Radix-nivå)
- **L3:** Multi-agent full autonomi, menneske = forretningsbeslutningstaker
- **L4:** Selvstyrende "self-steering" helt uten menneskelig inngripen i drift

### Språkgrensesnitt
Gartneren snakker med drivhuset via chat/RAG ("hvorfor stiger fuktigheten om natten?", "senk lyset 10 % i morgen").

### Dokumentert effekt i markedet
**Én dyrker styrer 40–50 ha (4×), opptil +10 % operativ profitt med −5 % ressursbruk** (Blue Radix Crop Controller).

---

## Oppsummering av mulighet
Markedet er i et teknologi-skifte fra regelbasert styring til AI-overlay på eksisterende HW — akkurat det en agentic-løsning kan utnytte uten å kreve ny maskinvare.

---

# Del 2 — Konkurranselandskap: hvem gjør dette allerede?

Kartlegging av hvem som allerede bygger hver del av den foreslåtte agentic-arkitekturen.

## Lag-for-lag: hvem ligger hvor

### Lag 1 – Sensing/IoT (datainnsamling)
- **Koidra DataPilot** — integrerer legacy-kontrollsystemer, henter data fra industri-sensorer, skyrå lagret/visualisert
- **Blue Radix** — Azure IoT-løsning, henter data fra diverse klima-computere
- **30MHz, Aranet**, etc. — IoT-sensorplattformer

### Lag 2 – Persepsjon/VLM (plantevision)
- **IUNU LUNA** — rail-monterte kameraer som ser *hver eneste plante*, maskinlæring til yield-forecast, "closed-loop plant-level vision" (330 % vekst i vine-crop-segmentet; $20M funding apr 2025)
- **Ecoation** — computer vision + IPM for tidlig skadedyr/sykdomsdeteksjon (whitefly-deteksjon per hus/rad)
- **Koidra** — kameraer brukes til å gjenkjenne avlingens status
- Forskning: AGRI-BT (VLM/CLIP disease detection), YOLOv8-avlingssykdomsdeteksjon

### Lag 3 – Reasoning/LLM-agenter (intelligensen)
**AI-overlay-selskapene (kjøres oppå eksisterende HW):**
- **Source.ag** — "digital co-pilot", AI for klima/irrigasjon/arbeid/crop-strategi. 300+ drivhus, 2 500+ ha, 18 land. Har AI-modeller for yield-forecast, setpoint-anbefalinger, anomali-flagging
- **Blue Radix Crop Controller** — autonomt styrer klima + irrigasjon, 5-minutters setpoints, "digital brain"; en dyrker styrer 40–50 ha, +10 % profitt, −5 % ressurser
- **Koidra KoPilot** — physics-informed, model-based reinforcement learning (MBRL); hierarkisk 3-lags styring (taktisk/daglig → operasjonelt/5-min → real-time via Hoogendoorn). Vant Autonomous Greenhouse Challenge, ~20 % utbytteøkning, 27,8 % netto-profitt

**Språkgrensesnitt / RAG-chat-agenter (gjør det jeg foreslo i "snakk med drivhuset"):**
- **Source.ag AskSource.ai** (mars 2025) — AI-copilot for growere, naturlig språk: høstingstid, klima, irrigasjon, beskjæring, 24/7
- **Quantum AI Copilot** (Polen) — bygget med LangChain + RAG + domain-tuned LLM, integrert mot **Priva/Hoogendoorn REST-APIer**, "strategy injection module" der grower definerer crop-plan; reduserer grower-involvering 10×
- **PhenoAssistant** (Nature Communications 2026) — samtalebasert multi-agent LLM for plantefenotyping
- Forskning AgroLLM, IPM-AgriGPT, m.fl.

### Lag 4 – Aktuering via API (kobler AI til klimakomputer, ingen HW-bytting)
- **Source.ag → Priva Connext** — Source beregner optimal strategi, Priva Connext utfører i drivhuset
- **Source.ag Irrigation Control → Priva PIM** — sensorer → skyberegning → auto-utførelse
- **Quantum Copilot → Priva/Hoogendoorn REST-APIer**
- **Koidra → Hoogendoorn** (real-time laget), **Koidra ↔ Priva**
- **Blue Radix → diverse klima-computere**

### Lag 5 – Safety/Governance (menneske-i-løkken, policy-grenser)
- **Blue Radix** — grower setter crop-strategi, AI realiserer; "Autonomous Greenhouse Manager" (fjern-menneske) overvåker 24/7
- **Quantum** — strategy injection-modul holder beslutninger i tråd med menneskelig intensjon
- **Forskning (ScienceDirect ASA)** — RAG-grounded LLM-agenter med *policy-gates, sensorvalidering, terskel-hysterese, offline-fallback*, tydelig human-oversight
- **Microsoft Copilot/AgriERP** — "assist → co-manage"-trapp, klare policy-grenser

---

## Gapanalyse: hva mangler i markedet?

| Foreslått kapabilitet | Status |
|---|---|
| RAG-chat / språkgrensesnitt | ✅ Finnes (AskSource.ai, Quantum, PhenoAssistant, AgroLLM) |
| Autonom klimastyring (setpoints) | ✅ Finnes (Blue Radix, Koidra KoPilot, Source.ag) |
| Autonom irrigasjon/fertigation | ✅ Finnes (Source Irrigation Control, Blue Radix) |
| Energioptimalisering mot strømpriser | 🟡 Delvis (Koidra/prisa, Blue Radix) — ikke fullt integrert med agenten |
| Plantevision / sykdomsdeteksjon | ✅ Finnes (IUNU LUNA, Ecoation) — men separat leverandør |
| Aktuering via API (ingen HW-bytting) | ✅ Modent (alle AI-lagene gjør dette) |
| Én orkestrerende **LLM-multi-agent** som dekker alle domener | ❌ Stort sett **ikke** integrert |
| Selvlærende / deep RL-løpende forbedring | 🟡 Koidra (MBRL) — få andre |
| Logistikk/arbeidsplanlegging-agent | 🟡 Svakt / fragmentert (Source.ag har deler) |

## Konklusjon
**Hver enkelt byggekloss finnes allerede** — men de lever i **siloer** fra ulike leverandører. Ingen har i dag en komplett, orkestrert **LLM-multi-agent** som dekker klima + energi + irrigasjon + helse + logistikk samtidig, med ett språkgrensesnitt og automon aktuering.

Nærmest det "fulle agentic-drivhuset":
1. **Source.ag** (+ AskSource.ai) — tettest på: co-pilot-språk + autonome moduler + Priva-aktuering
2. **Koidra** — sterkest innen autonom RL-kontroll + selvforbedring
3. **Blue Radix** — markedsleder på autonom growing i skala
4. **Quantum-copiloten** — beste referanse på en *tilpasset* LLM-agent koblet til klimakomputer-API
5. Forskning (ScienceDirect ASA) — nærmest min arkitektur rent konseptuelt (RAG-chat-agent + telemetri/aktuering-agent + n8n-orkestrering + policy-gates)

**Mulighet/posisjonering:** Det finnes et klart tomrom for en *leverandør-uavhengig multi-agent-orkestrator* som binder hele stacken sammen med ett språkgrensesnitt og policy-gated autonomi — dette er differensieringspunktet hvis du vil bygge noe selv.

---

# Del 3 — Konkurransematrise (produkt mot arkitektur-lag)

Leseveiledning: ✓ = modent/har det · 🟡 = delvis/i utvikling · — = ikke kjent levert · *≤2026*

## Topprissammendrag

| Selskap / produkt | Type | Scale/finansiering |
|---|---|---|
| **Blue Radix Crop Controller** | Autonomous growing (AI-tjeneste, ingen HW) | Globalt, markedsleder |
| **Source.ag** (Workspace, AskSource.ai, Irrigation, Harvest Forecast) | Software-only, vendor-nøytral AI | 300+ drivhus, 2 500+ ha, 18 land; ~$60M |
| **Koidra** (KoPilot, DataPilot) | Physics-informed RL-autonom kontroll | NV/Amerika; vant Autonomous Greenhouse Challenge |
| **IUNU LUNA** | Computer vision (plante-sensor) | NV/America+Europa; $65M totalt |
| **Quantum AI Copilot** | Tilpasset LLM-agent (RAG) | Prove-av-konsept (Polen) |
| **Priva One / Connext** | Inkumbent kontroll-OS + HW | 100+ land |
| **Ridder Hortimax Pro** | Inkumbent kontroll-OS + HW | Globalt |
| **Hoogendoorn IIVO** | Inkumbent neste-gen (autonomt fokus) | 100+ land |
| **Argus TITAN 900 / Axia** | Inkumbent kontroll (forskning/kommersiell) | Nord-Amerika |

## Lag-dekning mot den foreslåtte agentic-arkitekturen

| Kapabilitet | Blue Radix | Source.ag | Koidra | IUNU | Quantum | Priva One | Ridder | Hoog | Argus |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **L1 Sensing/IoT-data** | ✓ | ✓ | ✓ (DataPilot) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **L2 Plantevision (VLM)** | — | 🟡 | 🟡 (kamera) | ✓ | — | ✓ (PIM-vekt) | — | — | 🟡 |
| **L3a RAG-chat/LLM-agent** | 🟡 | ✓ (AskSource.ai) | — | 🟡 | ✓* | 🟡 | — | 🟡 | — |
| **L3b Autonom klima** | ✓ | ✓ | ✓ (best, RL) | — | — | ✓ (regelbasert) | ✓ | ✓ | ✓ |
| **L3c Autonom irrigasjon** | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **L3d Energioptimalisering** | ✓ | 🟡 | ✓ | — | — | ✓ (ECO) | 🟡 | 🟡 | 🟡 |
| **L3e Crop-strategi/forecast** | ✓ | ✓ (Harvest Forecast) | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | — |
| **L4 Aktuering via API (HW-agnostisk)** | ✓ | ✓ (Priva) | ✓ (Hoog/Priva) | ✓ | ✓* | — (eier egen HW) | 🟡 | 🟡 | 🟡 |
| **Selvlærende (RL)** | 🟡 | — | ✓ (MBRL, best) | — | — | — | — | — | — |
| **Menneske-i-løkken / strategi-innspill** | ✓ | ✓ | ✓ | — | ✓* | ✓ | ✓ | ✓ | ✓ |
| **Multi-agent-orkestrering (full stack)** | — | 🟡 | — | — | — | — | — | — | — |

## Hvem dekker hvilket autonomi-nivå (L0–L4)

| Nivå | Beskrivelse | Aktører |
|---|---|---|
| **L0** | AI gir råd → dyrker godkjenner | Source.ag (Workspace), Quantum, IUNU (anbefaling) |
| **L1** | Auto-anbefalinger med godkjenningsflyt | Source.ag, Blue Radix (tidlig fase) |
| **L2** | Autonom styring innenfor policy-grenser | **Blue Radix**, **Source Irrigation Control**, Koidra KoPilot |
| **L3** | Multi-agent autonomi, menneske = forretningsbeslutter | Delvis: Research (ScienceDirect ASA); ingen kommersiell komplett |
| **L4** | Full self-steering | **Koidra** (tettest — RL + hierarkisk styring, men én-agent) |

## Fag-spor: hvem gjør plantevision og LLM-agenter (utenom leverandørene)

| Type | Aktør | Status |
|---|---|---|
| Computer vision sykdom/skadedyr | **Ecoation**, IUNU, YOLOv8-forskning | Kommersiell + forskning |
| Konversasjonell multi-agent phenotyping | **PhenoAssistant** (Nature Comms 2026) | Forskning |
| RAG-grounded LLM-agenter for drivhus | **ScienceDirect ASA** (2026) | Forskning (nærmest fulle arkitekturen) |
| LLM-driven Behavior Tree-robotikk | **AGRI-BT** (2026) | Forskning |
| Fakultativ agro-LLM | AgroLLM, IPM-AgriGPT | Forskning |

## Tomrom — ingen dekker i dag (bekreftet)

1. **Én orkestrerende multi-agent** som dekker klima + energi + irrigasjon + helse + logistikk samtidig
2. **Ett språkgrensesnitt** over hele verktøystakken (ikke bare klima/irrigasjon)
3. **Policy-gated autonomi + logging** som standard-modul i kommersielle produkter
4. **Selvlærende (RL) kombinert med LLM-orkestrering og plantevision** i ett produkt
5. **Logistikk/arbeidskraft-agenter** (fragmentert i dag)

# Del 4 — Edge AI, World Model, Digital Twin, Simuleringsfabrikk & Rekursiv læring (human-in-the-loop)

Vi utvider den agentic-visjonen til en komplett, selvforbedrende "lærende fabrikk" for drivhus, der menneske alltid sitter i førersetet.

## 4.1 Den konsoliderte arkitekturen (revidert)

```
                    ┌─────────────────────────────────────────────────────┐
                    │                 MENNESKE (human-in-the-loop)        │
                    │  setter crop-strategi, mål, policy, godkjenner,     │
                    │  validerer, håndterer unntak, eskalerer autonomi    │
                    └───────────────┬─────────────────────────────────────┘
                                    │ intensjon / mål / policy
            ┌───────────────────────▼───────────────────────────┐
            │   ORKESTRERENDE MULTI-AGENT (LLM)                 │
            │   Chat-agent · Climate · Energy · Irrigation ·    │
            │   Health/VLM · Logistics · Safety-agent           │
            └───────────────────────┬───────────────────────────┘
        foreslåtte setpoints/planer  │           observert tilstand
┌───────────────────────────┐        │        ┌──────────────────────────────────┐
│  EDGE AI (lokalt i huset) │◄───────┴───────►│ WORLD MODEL (lært dynamikk)       │
│  inferens: detektér/dose  │  beslutning     │  predikerer avling/klimareaksjon  │
│  offline, lav latens,     │  handler        │  ← renteres kontinuerlig av data │
│  MQTT/REST/OPC-UA →       │                 └───────────────┬──────────────────┘
│  klima-computer           │◄─── aktuerer ────│               │ oppdaterer
└───────────────┬───────────┘                 └───────────────▼──────────────────┐
                │                                DIGITAL TWIN (høy-fidelitet)      │
                │  sanntids sensordata ─────────► rekonstruerer fysisk drivhus     │
                │                        ┌────── decompilerer/validerer ──────────┘
     FYSISK DRIVHUS: sensorer, kamera,
     roboter, klimakomputer              ▲
        │ observasjoner                   │ nye erfaringer mates tilbake
        │  ▼                              
┌───────┴───────────────────────────────────────────────────────────────────────┐
│  SIMULERINGSFABRIKKEN (sim-to-real)                                            │
│  syntetisk data → RL-trening → domanerandomisering → MiL→HiL→ViL → trygg       │
│  distribuering · polisier produseres/valideres i sim før kontakt med virkelighet│
└───────────────────────────────────────────────────────────────────────────────┘
        ▲ rekursiv læring: erfaring fra drift → twin/world-model → bedre sim/policy
```

**Ett sett regler: alt går gjennom mennesket.** Agen ten foreslår og utfører innenfor policy-gjerder; mennesket definerer hva som er bra (reward/strategi), godkjenner autonomi-nivå og bekrefter nye policyer før de slippes løs.

## 4.2 Edge AI — AI kjører der beslutningen skjer

- **Konsept:** Inferens lokalt på enhet/til / nær data-kilden — i stedet for sky. Kameraer, sensorer, roboter og en drone mater en lokal "edge AI-computer" (på radslutten/interne) som detekterer, analyserer, bestemmer og handler lokalt; skyen brukes til dashboards, modelle-oppdateringer og flåtestyring.
- **Hvorfor (drivhus):** Sykdomsdeteksjon må flagge et blad *mens kameraet er foran det*; kvalitetsinspeksjon på sorteringsbånd må holde tritt med beltet; et autonomt kjøretøy på skinne kan ikke pause for å spørre skyen. Kort: **latensvinduer måles i plantens/maskinens fart**.
- **Gevinst:** lav og stabil latens, offline-drift (overlever internettbrudd), data slippes ikke av gårde (personvern), gjentakende skyavgifter → engangs-HW-kost.
- **2026-status:** HW moden (NVIDIA Jetson Thor, Google Coral, Hailo-8L, Raspberry Pi 5); 7–8 mrd-parametere LLM kjører on-device med sub-50ms latens. INT4/8-kvantisering, prunning, knowledge distillation.
- **Referanse-arkitektur (Growmatics):** kamera/sensor → Edge AI (detekter/klassifiser/mål) → besluttningsmotor (regler/terskler) → robot/klima-controller → sky-synk. **Protokoller:** MQTT (lav-last, tåler dårlige linker), REST, **OPC-UA** (industristandard for klimacomputere), lokal edge-database som buffer ved brudd.
- **Split inference:** edge gjør preprocessing/sensing; sky gjør «rettingen»/kompleks analyse. Edge→LLM: lokale små-språkmodeller for "spør stedet" i klarspråk.

## 4.3 World Model — den lærte dynamikken i drivhuset

- **Konsept:** En modell som *lærer* hvordan miljøet responderer på handling (action-conditioned) — ikke en statisk formel. Brukes til å **forutse konsekvenser av handlinger før de utføres**.
- **For LLM-agenter (forskningsfronten):** *Reinforcement World Model Learning (RWML, arXiv 2026)* — lærer action-conditioned world models for LLM-agenter med *sim-to-real gap reward*, slik at agenten kan forvente konsekvenser og tilpasse seg miljø-dynamikk i stedet for å bare "prate".
- **I drivhuset:** world model predikerer hvordan avlingen og klimaet responderer på setpoints (lys, varme, CO2, vann); ag entene simulerer "hva skjer hvis jeg dimmer 10 %" lokalt og raskt.
- **Rentring:** modellen oppdateres kontinuerlig fra drift-data — dette er forbindelsen til rekursiv læring.

## 4.4 Digital Twin — høy-fidelitet replika kontinuerlig oppdatert

- **Konsept:** En gjenskaping av det fysiske drivhuset (multifysikk) som mottar sanntidsdata og simulerer scenarier. Dermed kan kontroll-taktikk testes **uten å berøre det ekte drivhuset** — en "safe sandbox" for hva-hvis-analyser.
- **I litteraturen:**
  - *Reinforcement learning-based Digital Twins in agriculture* (2024) — RL-agentens kvalitet avhenger av hvor godt miljøet er modellert; funksjonerende twin møtes av reelle erfaringer mates tilbake → modeller/simulasjoner oppdateres.
  - *Digital Twin med online ML for autonom drivhus-klimastyring* — IoT-sensing + hybrid-modellering + dyp RL i ett.
  - *Hybrid Digital Twin for drivhus og underjordiske miljøer* (IEEE 2024), mobile-network DT-rammeverk.
  - *Digital Model Playground (DMPG)* — simuleringsmiljø for å integrere RL med digital-twin-optimering.
- **Kommersielt:** svært lite; twin er i dag mest forskning og tidlig fase (Koidra kaller sin data-lagde "digital twin" som trinn 2 i deploy-reisen).

## 4.5 Simuleringsfabrikken (sim-to-real-produksjonslinje)

- **Konsept fra industri (Siemens/Delft sim2real, bl.a. autonom bil):** RL-trening skjer først i simulering (billig, rask, labeled, mange kritiske scenarier), deretter overføres til virkeligheten i stadier **MiL → HiL → ViL**.
- **Simuleringsoptimiserings-skjevhet ("sim2real gap"):** en policy kan utnytte feil i simulatoren og over-vurdere egen ytelse. Motvirkes med **doma-nerandomisering (DR)** + **doma-nadaptasjon (DA)** + høy-fidelitet-modeller.
- **Simuleringsfabrikk for drivhus = industrialisert pipeline** som *produsere* validerte policyer/scenarier kontinuerlig:
  1. syntetisk datagenerering (millioner av scenarier, sesonger, klima-variabler, sykdoms-tilfeller)
  2. RL-trening mot digital twin / hybrid-modell
  3. doma-nerandomisering for robusthet
  4. scenario-bibliotek + "regresjon": feil fra produksjon/eksperimenter mates tilbake i simulsamlingsbiblioteket
  5. kvantorvalidering (MiL→HiL→ViL) før trygg release til ekte drivhus
- Dette er kjernen i å kunne frigjøre *AI i produksjon* trygt og skalerbart.

## 4.6 Rekursiv læring — selvforbedrende sløyfe

- **Sløyfen:** reell erfaring → tilbakeføring til digital twin + world model → bedre simulering → bedre policy → tilbake i produksjon. Hver runde gjør systemet bedre til å lære.
- **Koidra** er kommersielt nærmest: *model-based reinforcement learning* med eksplisitt "Autonomous Continuous Improvement"-fase (imitation-learning-init, hierarksk styring, kontinuerlig optimalisering) — "Digital Twin"-trinn + RL-tilnærming.
- **Forskningsgrunnlag:** RL-based digital twins i landbruk; RWML for LLM-agenter; hybrid-modellering og sim2real med DR/DA.
- **Resultat:** systemet lærer av hver driftsdag, avik, og hvert dyrkeprojekt; agetene blir bedre å planlegge, og den menneskelige dyrkerens strategi-innsikt "lagres og forsterkes" i policyene.

## 4.7 Human-in-the-loop-styring — "human in the lead"

- **Mennesket definerer alt som betyr noe:** crop-strategi, økonomiske mål, bærekraftskrav, reward-funksjon, autonomi-nivå, policy-grenser, compliance-grenser.
- **Agen foreslår → menneske godkjenner / eskalerer.** Alle nye policyer valideres (MiL→HiL→ViL) og bekreftes av menneske **før** de slippes løs på ekte drift.
- **Safety-lag:** policy-gates, sensorvalidering, terskel-hysterese, offline-fallback (ScienceDirect ASA-modellen), full logging, exception-håndtering; fjern-"Autonomous Greenhouse Manager" overvåker 24/7.
- **Tillits-stige:** L0 (råd) → L1 (godkjenning) → L2 (autonomi i gjerder) → L3–L4 (multi-agent full autonomi), hver eskale-krever menneske-bevis og tillit-data.
- Regulativt & kommersielt nødvendig — grower-tillit er den største adopsjons-takten i markedet.

## 4.8 Markedsstatus for utvidede konsepter

| Konsept | Status 2026 | Aktører / referanser |
|---|:---:|---|
| Edge AI i drivhus | 🟡 Tidlig kommersiell | Growmatics (referanse-arkitektur), forskning; HW moden 2026 |
| On-device/edge LLM (7–8B) | ✓ Moden HW | Jetson Thor, Coral, Hailo; kvantisering (INT4/8) |
| Digital Twin drivhus | 🟡 Nesten bare forskning | RL-based DT (2024), online-ML DT, hybrid DT, DMPG |
| World model for LLM-agenter | 🔬 Forskning | RWML (arXiv 2026) — komplett nytt |
| Simuleringsfabrikk / sim-to-real | 🟡 Mest industri (bil) | Siemens/Delft; i landbruk: hybrid sim2real, "playground" |
| Rekursiv / RL <br>selvforbedring | 🟡 Koidra er nærmest | Koidra MBRL "Autonomous Continuous Improvement" |
| Human-in-the-loop | ✓ Modent mønster | Blue Radix, Quantum, ScienceDirect ASA (policy-gates) |

## 4.9 Tomrommet (oppdatert)
Ingen kommersiell aktør kombinerer i dag: **edge-AI-drift + lært world model + kontinuerlig oppdatert digital twin + industrialisert simuleringsfabrikk + rekursiv selvlæring**, alt samlet under **én orkestrerende LLM-multi-agent** — med mennesket som definerer strategi og godkjenner autonomi. Det er det helhetlige "lærende drivhus"-målet dette dokumentet peker på.

> **Notat:** Konseptene her (edge, twin, factory, runtime-core + agen-orkestrering, human-in-the-loop) speiler naturlig de repo/byggeklossene du allerede har i din egen valo-plattform (`valo-edge`, `Valo-Twin`, `valo-factory`, `valo-runtime-*`). Drivhuset er dermed et svært godt *referanse-domene* for å validere den plattformen.

---

# Del 5 — Aktiv-/sendemåler-sensing: signal som reflekteres (GPS-gjennom-io"NB: sender ut et signal og leser refleksjonen")

Siste byggestein. Vi vurderer alle modaliteter der systemet **sender ut et signal (EM / akustisk / stråling) og tolker refleksjonen** — droner/mikro-droner, skanning, Wi-Fi-sensing (RuView), ultralyd, røntgen "u name it".

> Merknad om passiv vs. aktiv: multispektral/NDVI fra droner er **passiv** (tolker *reflektert sollys*); Wi-Fi/RF, radar/mikrobølge, terahertz, ultralyd og røntgen er **aktiv** (sender egen kilde + leser refleksjon).

## 5.1 Konsept og felles prinsipp
Alle disse leser en **kanalendring** i et reflektert signal forårsaket av et biologisk mål (plante, blad, stamme, frukt, person, skadedyr). Felles ligger: billig/integrert sensor → lokal (edge) signalprosessering/DSP → modell (maskinlæring) → "ruktor" inn til perception-laget. Dette styrker persepsjonen uten å avhenge av lys/vær og inn i det som er usynlig fra overflaten.

## 5.2 Modalitet-for-modalitet: send brillanten, les refleksjonen, retur av hva

| Modalitet | Signal det sender | Hva det leser/reflekteres | Ubruksår |
|---|---|---|---|
| **Wi-Fi / RF-sensing (CSI, f.eks. RuView)** | Radio (Wi-Fi, CSI på subcarriere) | Endring i utbredelsesvei: tilstedeværelse, bevegelse, pust/hjerte (vital-signs), aktivitet, RF-fingeravtrykk av rom | Billig, kontaktfri, kameraløs, prinsippbasert; brukt for mennesker — overførbart til plante/tak/labour |
| **RFID / backscatter** | Radio-modulert mikro-refleksjon | Passiv, chipseless sensor: vannstatus i plante via dielektrisk forandring | Ekstremt billig, kontakt/minimal, passiv|
| **Mikrobølge / FMCW-radar** | Mikrobølge (kontaktfri resonans) | Vanntrykk/vanntilstand i stamme/blad (dielektrisk), respirasjon | Kontaktfri, dypere enn overflatesensorer |
| **Terahertz (THz)** | THz-bølger (0,1–10 THz) | Vanninnhold/vanntrykk gjennom *hele tverrsnittet* av bladet (hydrogenbinding-sensitive) | Ikke-ioniserende, penetrerer, robust mot miljø-variasjon |
| **Ultralyd** | Høyfrekvent lyd → primærekko | Vannforandring i stamme (ekkoposisjon, AIC-algoritme), NC-RUS på blad; akustisk bildesetting | Ikke-destruktiv, hurtig, kontaktfri (NC-RUS); trenger dyplæring/kalibrering, begrenses av tykk stamme/demping |
| **Røntgen (X-ray / CT)** | Ioniserende stråling | Indre fruktkvalitet/defekter (tetthetsforskjell -> gråtoner), browning/cavities | Ikke-destruktiv, rask (CT ~90%+, 2D-røntgen ~10 s), best for sortering på pakkelinje |
| **Droner/mikro-droner** | (Multispektral/hyperspektral/LiDAR/termisk — passiv m.v. cam) | NDVI/NDRE, stress, skadedyr, canopy, 3D, varmeansier; mikro-droner under canopy/mellom blad; svarm | Bredt nett-bilde, romlig; inne i drivhus (f.eks. til SO-agn og predator-interception) |

## 5.3 Vurderingstabell (for et agentic-drivhus)

| Egenskap | Wi-Fi/RF CS | RFID/backscel | Mikrobølge/radar | THz | Ultralyd | Røntgen | Droner/mikro |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Kost per node** | ~$9 (ESP32-S3) | Svært lav | Lav–mellom | Høy (forsknings/niche) | Lav–mellom | Høy (rust + stråling) | Lav–høy (per drone) |
| **Nøyaktighet/oppløsning** | Grov (tilstedev./aktivitet) | Grov (ja/nei på state) | Mellom | Mellom–høy | Mellom–høy | Høy (indre) | Høy (romlig/NDVI) |
| **Penetrering (dybde)** | Gjennom rom/tak | Overflate/kort | Stamme/blad* | Kreis-tverrsnitt blad | Stamme/blad | Inne i frukt | Overflate (canopy) |
| **Invasivitet** | Berøringsfri | Minimal | Berøringsfri | Berøringsfri | Berøringsfri* | Berøringsfri men ioniserende | Berøringsfri |
| **Primær driftskontekst** | Inne (rom/labour) | Plante/kanister | Plante-vann | Blad | Plante | Pakkelinje (post-harvest) | Hel-rom, scouting |
| **Modenhet (2026)** | 🟡 Moden (mennesker), ny for planter | 🟡 Forskning | 🟡 Forskning | 🔬 Forskning | 🟡 Forskning/tidlig | 🟡 Moden (sortering) | ✓ Moden (felt), 🟡 inne i drivhus |
| **Edge-kompatibel** | ✓ (kjører på edge, ESP32/R-Pi) | ✓ | ✓ | 🟡 | ✓ | 🟡 | 🟡 (bilder til edge/cloud) |
| **Human-in-the-loop-verdi** | Besetning/labour/aktivitet | Plantehelse | Vann-IR | Vann-IR | Vann-IR | Kvalitet/sortering | Skadedyr/tidlig stress |

## 5.4 Øyeblikkelig anbefaling for det "gendrivningsbare" agentic-drivhuset

**Høyk bun er å dekke kontinuet: eksternt-oks-syn (droner) + inne-vann/aktivitet (RF/Wi-Fi) + indre frukt (røntgen på pakkelinje):**

1. **Wi-Fi/RF (RuView-lignende, CSI) — "rom-faunen"** → tryggade billig lag: labour/tilstede-føring, robot-posisjon, RF-fingeravtrykk-forandring i drivhuset (nytt objekt, aktivitet, growth-rate via indirekte signalforandring). Edge-first, ~$9/node, private.
2. **Droner + mikro-droner (multispektral/thermal/LiDAR + svarm)** → skadedyr/stress-overvåking i skala; mikro-droner under canopy/mellom blad; på sikt svarm + predator-interception (teknisk kontekst i litteraturen). Kobles til persepsjons-/VLM-laget og sharp-Source/Blue-Radix posisjonering.
3. **Ultralyd / THz / mikrobølge (plante-ether team)** → kontinuerlig, ikke-destruktiv plasse- og vannstatus der det er dyrt-kritisk (vann-ledere, tomats/strawberry) — gir verdi til irrigasjons-/fertigation-agenten.
4. **Røntgen (CT/2D) på pakkelinje** → intern fruktkvalitet/distans-sortering (pære/epler/sitrus/avocado), ~90–99 % nøyaktighet med dyp-læring; driver kvalitets-/logistikk-agenter og premium-prising.
5. **RFID/backscatter (passiv)** → lavkost "money-mesh" på enkeltplanter/kanaler for diskret state-trekk, god til å validere twin-modeller.

Alle mates tilbake i perception-laget → world model → digital twin → simuleringsfabrikk (som kan syntetisk generere *sensor-signaler* for å trene modellene, inkl. X-ray/ultralyd output) → rekursiv læring, med menneske som godkjenner hver ny modell/policy.

## 5.5 Integrering i den konsoliderte arkitekturen

```
        Aktive sendesensore (sender signal → leser refleksjon)
   Wi-Fi/RF · RFID · mikrobølge/radar · THz · ultralyd · røntgen · droner/mikro
                 │  råsignal
                 ▼
        [EDGE AI/DSP & skade-rätning]  (filter, domenadaptasjon, ML, fusions)
                 │  semantikk (vannstatus, skadedyr, aktivitet, fruktdefekter)
                 ▼
        [PERCEPTIONS-/VLM-LAGET]  ──► [WORLD MODEL] ──► [DIGITAL TWIN]
                                                          │
                                                          └─► [SIMULERINGSFABRIKK]
                                                              (genererer syntetisk
                                                               signal-data for trening)
                 ▲
        MENNESKE: godkjenner modeller/policyer, setter grenser
```

**Viktig for "Cutting edge":** De fleste av disse (Wi-Fi/RF på planter, THz på blad i felt, X-ray-DL i inline) er i dag *forskning*, ikke kommersielle plattformer. Det gir et åpent rom å bygge et *sensor-agnostisk, sammensatt perception-lag* som banker alle disse sammen — noe ingen leverandør (Blue Radix, Source.ag, Koidra, IUNU) gjør i dag. Flere av dem begrenser seg til én modalitet (IUNU=vision, Koidra=klasse-sensor+IoT, Blue Radix=klasse/irrigasjon). Her ligger den bredden et fremtidig agentic-drivhus kan differensiere seg med.

## 5.6 Rask modenhet- og aktøris-kart

| Modalitet | Modenhet | Ledende miljø |
|---|:---:|---|
| Wi-Fi CSI (RuView) | 🟡 (mennesker) | ruvnet RuView, ESP32/rvcsi, Nexmon (kilo-$-nodes) |
| RFID/backscatter-behov | 🟡 | Forskning (passiv "chipløs" mikrobølge-spiral) |
| Mikrobølge/radar | 🟡 | Univ. Pisa/CNR m.fl. |
| Terahertz | 🔬 | Springer THz-forskning (leaf water non-contact) |
| Ultralyd/NC-RUS | 🟡 | GOFAR/Robagri, forskning (thermal-drop) |
| Røntgen/CT (frukt) | 🟡→✓ | KU Leuven MeBioS, MDPI (pear/apple/citrus/avocado) |
| Droner/mikro multisp+termisk+LiDAR | ✓ (felt), 🟡 (inndriv) | DJI, AeroVirtual de PL-former; forskning på greenhouse-droner + svarm/predator |

---

# Del 6 — POC / byggeplan (minimalt, validerbart, fase-inndelt)

Forutsetning: vi bygger **det minste meningsfulle systemet** som beviser at lagene fra Del 4 + 5 henger sammen på data, ikke på papir. Hvert fase-mål har en eksplisitt **exit-criterion** (hva som må stemme før vi går videre).

## POC-mål og avgrensning

- **Mål:** et *leverandør-uavhengig* "snakk med drivhuset"-system som (a) samler sensor-signaler fra fler-modale kilder, (b) lar en menneskelig dyrker spørre naturlig-språk-LLM og få svar forankret i egen data (RAG), og (c) *foreslår* (og i siste fase utfører innenfor policy) klimatiske plan — alt logget og human-godkjent.
- **Ikke på POC-scope:** full multi-agent autonomi, egen HW-klimacomputer, X-ray-inline, produksjons-plattform. Kun en **referanse-enhet** (1 drivhus/parsell eller en laboratorie-miniatyr-drivhus, som i sim2real-forskningen).
- **Drivhus-tilnærming:** bygge på **eksisterende klima-computer via API** (Priva/Ridder/Argus/Hoogendoorn REST/OPC-UA) — ingen installasjon av ny kontroll-maskinvare.

## Byggesteinvalg (tech stack, forslag)

| Lag | Valg |
|---|---|
| Edge-node | Jetson Orin-Nano / Raspberry Pi 5 + Coral/Hailo (±ESP32-S3 mesh for CSI) — kjører inferens + DSP |
| Signalinnsamling | MQTT (lav-last, tåler ujevn link); OPC-UA → klimacomputer; REST for konfig |
| Orchestrator | **n8n** (lav-kode workflows — som i ScienceDirect ASA-referansen) |
| LLM/RAG | Lokal/open (7–8B on-device, f.eks. kvantisert) + vektor-db (Qdrant/Chroma) med SOP/manual/vekstdata |
| VLM/perception | Åpne visjonsmodeller for plantehelse + egne trenede klassifiserere for Wi-Fi-CSI- og ultralyd-signaler |
| Data/twin | Tidsserie-lagring (TSDB/InfluxDB) + enkel hybrid-modell (fysikk+lært) for klimat/digital-twin |
| Simuleringsfabrikk | Mini-drivhus-simulator (hybrid PBM/LSTM/RL-løkke) med dopaminrandomisering |
| Policy-gates | Regel-motor i workflow + log (audit), offline-fallback i edge |
| Human-gate | Godkjennings-UI (naturlig-språk): foreslått sett → dyrker OK → utfør |

## Faser og exit-criteria

**Fase 0 — Grunnmur & data** (2–4 uker)
- Koble 1 klimacomputer via OPC-UA/REST; edge-node kjører MQTT-broker.
- Strøm: temperatur, fukt, CO2, lys, irrigasjon + kamera + (valgfritt) 1 RuView-lignende CSI-node + 1 ultralyd/NC-RUS-probe.
- Bygg datasett + grunnlinje telemetri i 2 uker.
- ✅ **Exit:** stabil, timestamped tidsserie; alle modaliteter logges; klart "ground-truth"-notat (menneskelig definert, hva "bra" er).

**Fase 1 — Multi-modalt perceptions-lag** (4–6 uker)
- Tren/justér: (a) plantehelse-VLM, (b) skade-/stress-diskriminering fra CSI-mønster, (c) vannstatus fra ultralyd, (d) plus kamera-NDVI via mikro-drone (manuelt/autonomt). Fusjon av signalene i ett semantisk "tilstandsbild".
- ✅ **Exit:** modellene klassifiserer holdbare utfall (f.eks. fukt-lag vannstatus ±10 %, skadedyr-flagging ≥90 % av manuell verifikasjon) på ubrukt holdout-data.

**Fase 2 — RAG-chat-copilot (L0→L1)** (3–4 uker)
- Bygge "AskTheGreenhouse.ai"-kopi: LLM (lokal/edge) + RAG over SOP-er/manualer + live telemetri-kontekst.
- Dyrker spør: «hvorfor stiger fuktigheten i natt?», «hva er risikoen for pulver-mugg i morgen?». Foreslår setpoints; dyrker godkjenner; ingenting utføres automatisk.
- n8n-orkestrering + auditable policy-gates + logging.
- ✅ **Exit:** dyrker godkjenner svar ≥80 % av tiden som korrekt/nyttig på blindede spørsmål; foreslåtte setpoints innenfor sikre grenser.

**Fase 3 — Autonom vann/klima-modul (L2, avgrenset)** (4–6 uker)
- Kopi av Source Irrigation Control-oppsett: agen foreslår klimat/irrigasjonsplan via klimacomputer-API; **standard = godkjenningsmodus**, med "autopilot innenfor policy-gjerder" som valgfri modus i avgrensede enheter.
- Bygg world-model (predikter utfallet av 5-min-setpoint).
- ✅ **Exit:** i a/b mot menneskelig dyrker over ≥1 vekst-syklus: minst like bra yield, **mindre energi/vann per kg**, 0 policy-brudd (audit-bekreftet).

**Fase 4 — World model + digital twin + simuleringsfabrikk (sim2real)** (6–10 uker)
- Bygge hybrid-modell/twin (fysikk+PBM/LSTM) + mini-simulasjonsløkke; trene RL-policy i sim med dopaminrandomisering; validere via MiL→HiL→ViL-rekkefølge; test i mini-drivhus.
- Simuleringsfabrikken genererer *syntetiske sensor-signaler* (også ultralyd/lign.) for trening.
- ✅ **Exit:** sim-trent policy fungerer i mini-drivhus (sim2real-gap underkontroll), og digital-twin klart A/B-testbar.
- (Human-gate: Ny policy slippes kun etter menneske-godkjenning + ViL-kvittering.)

**Fase 5 — Rekursiv læring + multi-agent (L3–L4-kandidat)** (løpende)
- Sløyfe: drift-erfaring → tilbake i twin/world-model → bedre sim → bedre policy. Legge til agenter: energi (mot strømpriser), helse (skadedyr), logistikk.
- Flagg hver kompetanse-oppgradering til mennesket; bruk tillits-stige for å eskal-lere autonomi kun på data-bevis.
- ✅ **Exit:** dokumentert "kjente ukjente", system-lærer av feil, og minst én autonomi-eskalering gjort trygt (menneske-godkjent) over tid.

## Validering & QC (gjennomgående)
- **Ground-truth-notat** (hva "bra" er) defineres av mennesket først — reward-funksjonen bygges på dette.
- **Holdout-datasett** for hver modell; ingen all-validering på trening-data.
- **Audit-log** for alle setpoints, beslutninger, policy-brudd og godkjennelser (tillit- og regulativ-bevis).
- **Offline-fallback:** edge-node beholder siste gyldige policy ved nettbrudd.
- **Røde flagg:** hvis modellene ikke presiseres innen et fase-budsjett → stopp, hånd-overfør, revurdér scope.

## Risiko & åpne spørsmål
- Grower-tillit og forklarbarhet; modeller som fanger "overflate" i stedet for sanne biologiske triggers.
- Wi-Fi-CSI på planter er umoden — kan kreve egen dataproduksjon/annotering.
- X-ray er sen-fase (pakkelinje, egen strålings-HW) — eget side-POC.
- Datakvalitet/heterogen legacy-HW (API-tilgang varierer mye mellom leverandører).
- Energi-kobling mot sanntids strømpriser avhenger av lokale støttetjenester.

## Grove tidslinje- og ressursvirke
- Total ~6–9 måneder for **Fase 0–4** som fungerende POC; Fase 5 er løpende.
- Liten gruppe: 1 sensor/edge, 1 ML, 1 fullstack/LLM-orkestrator, + hoved-dyrker som produkt-eier og domene-ekspert.

## Hvorfor dette beviser noe som ingen gjør i dag
POC-en fletter sammen **flere aktive sensor-modier + RAG-LLM + policy-gated aktuering + trening i sim via digital twin** — den kombinasjonen og den bredden leverer ingen kommersiell leverandør i 2026 (Blue Radix=klasse/irrigasjon, Koidra=RL-kontroll, IUNU=vision, Source.ag=AI-overlay). Dette er et POC på det åpne "sensor-agnostiske, sammenslåtte" tomrommet, ikke en kopi.

---

## Kilder
- Marqstats: Global Greenhouse Management Software Market 2026–2030
- Dataintelo: Greenhouse Automation Market Report 2034; Greenhouse Products Market 2034
- MarkWide: Greenhouse Produce Market 2026 ($387,6 mrd → $870 mrd 2035)
- GPN Magazine: Greenhouse labor outlook for 2026; Automation and Climate Tech trends
- FinancialModelsLab: Greenhouse Farming Running Costs 2026
- Priva, Ridder, Hoogendoorn, Argus Controls (leverandørnettsteder)
- Blue Radix (Crop Controller), Microsoft customer story, GreenTech
- ScienceDirect: "An agent-based service architecture for smart greenhouses: RAG-grounded LLM agents" (2026); "AGRI-BT robot: LLM-driven behaviour trees" (2026)
- Richland / VerticalFarmDaily (2026-07)
- Nature / Springer: Smart greenhouse farming mot near-zero energy
- Source.ag (solutions, Irrigation Control, AskSource.ai), PR Newswire, Hort News
- IUNU (LUNA, how-it-works, $20M GeekWire 2025)
- Koidra (DataPilot, KoPilot, IESO Great Lakes rapport 2025, Autonomous Greenhouse Challenge)
- Quantum (AI Copilot for Greenhouse Operations — LangChain/RAG + Priva/Hoogendoorn API)
- Ecoation, Greenhouse Grower (What Can Growers Do With AI Now? 2026)
- Nature Communications: "A conversational multi-agent AI system for automated plant phenotyping" (PhenoAssistant, 2026)
- Microsoft Copilot / AgriERP (AI i landbruk 2024→2034, 26,3 % CAGR)
- Ecoation (Greenhouse Grower: computer vision for deteksjon av skadedyr/sykdom)
- IESO Grid Innovation Fund-rapport: "Energy-efficient AI-powered Autonomous Greenhouses" (Koidra × Great Lakes Greenhouses, 2025)
- Growmatics: "Edge AI for greenhouse automation" (2026, referanse-arkitektur; MQTT/REST/OPC-UA)
- Iterathon: "Edge AI & On-Device Inference 2026" (Jetson Thor, Coral, Hailo, INT4/8-kvantisering)
- GeniusTechLab: "Edge AI Inference in 2026" (7–8B LLM on-device, sub-50ms)
- ScienceDirect: "Edge AI-Enhanced Nodes for Intelligent Agricultural..."; "AIoT med optimal embedded edge intelligence" (2026)
- arXiv 2602.05842: "Reinforcement World Model Learning for LLM-based Agents" (2026)
- ScienceDirect: "RL-based Digital Twins in agriculture" (2024); "Digital twin framework for smart greenhouse management" (2024)
- IEEE 10534064: "Hybrid Digital Twin Model for Greenhouse and Underground..." (2024)
- arXiv 2211.14874 / IFAC 2023: "RL from Simulation to Real World Autonomous Driving using Digital Twin" (Siemens/Delft; DR/DA, MiL/HiL/ViL)
- arXiv 2510.23882: "Hybrid Modeling, Sim-to-Real RL..." (2025, mini-drivhus)
- Springer: "Digital Model Playground (DMPG)" — RL + digital-twin-simulering
- RuView / ruvnet (WiFi CSI-sensing, ESP32-S3, rvcsi edge runtime, Nexmon) + knightli.com guide
- MDPI Sensors 2026: "Deep-Learning-Based Baseline Evaluation of Public WiFi CSI Datasets"
- X-ray/CT frukt: KU Leuven MeBioS (pear/apple/citrus/avocado), MDPI Agriculture 2025, Springer J Nondestruct Eval 2026
- Droner: Advexure/DJI multispektral NDVI/NDRE, droneasaservice, agronomyjournals (micro-drones, swarm, predator-interception)
- Ultralyd: PMC (ultrasound primary echo, plant stem water, AIC), GOFAR/Robagri NC-RUS, Plant Methods
- Terahertz: Springer J Infrared, Millimeter & THz Waves 2025 (non-contact leaf water)
- Mikrobølge/radar: ScienceDirect (non-invasive microwave plant water stress, Univ. Pisa/CNR)
- Wiley JSFA 2026: "Assessing plant water status: Part 2 – non-destructive"
