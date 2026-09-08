# Synapse Lab — Forskingsnotat: P5-sweep → Synapse-tesen

Dato: 2026-08-04

## Koblinga

Synapse-tesen (README) seier: agentar av ulike modellar, med positiv forsterkning,
kan produsere innsikt som ingen enkeltagent finn åleine. Forståelsen ligg i rommet
mellom synapsane — i den emergente relasjonen, ikkje i eit sterkt enkeltutsagn.

P5-sweep-et i `Tofoo-/experiments/P5_Swarm_Coherence/` er den første kvantitative
målingen av den same typen påstand, på sværm-nivå. Forskingsbeslutning 2
(positiv forsterkning) og 3 (observasjon via Tofoo P12/P5) er dermed knytta saman.

## Kva P5-sweep-et viste (ærleg)

- Eksogent filter (Lovgiveren) → konsensus, monotont dose-respons i tolerance.
- NEGATIV KONTROLL (dummy-filter som berre loggar) = identisk med ingen filter.
  Kausal effekt kjem frå aktiv korreksjon, ikkje frå å ha filteret i loopen.
- Ved tolerance 5.0 (aldri grip inn) kollapsar resultatet til baseline.
- Konklusjon: konsensus kjem frå HANDHEVING av loven, ikkje frå sjølvorganisering.

## Konsekvens for Synapse-tesen

Dette er den viktigaste varsellampen: P5 viser at "struktur i relasjonane"
utan aktiv forsterkning gir ingenting. Synapse-tesen hevdar noko sterkare —
at forståelse oppstår i rommet mellom synapsane. For at tesen skal vere
meir enn ein omformulert "positiv forsterkning virkar", må den skilje mellom:

1. Effekt av relasjonsstrukturen (kven snakkar med kven, kva blir forsterka)
2. Effekt av total forsterkningsmengde (P5: dose-respons)

P12-designet (C0/C1/C3/C5) er nøyaktig dette skillet:
- C0 = ingen relasjon (enkeltnode)
- C1 = ensemble utan strukturert utveksling
- C3 = strukturert Synapse (relasjonell struktur)
- C5 = randomisert Synapse (relasjonell struktur men tilfeldig — NEGATIV KONTROLL
  på strukturnivå, analog til dummy-filteret i P5)

## Falsifikasjonskriterium for Synapse-tesen

MVP-beslutningsregelen i `Tofoo-/experiments/P12_Synapse_Test/`:

- C3 gir positiv gevinst i minst 3 av 4 familiar (T1–T4)
- OG C3 slår C5 på T1 og T2

Dette er det minste kravet for å skilje relasjonell struktur frå tilfeldig
struktur, og dermed frå "berre mykje forsterkning". Utan at C3 > C5, er tesen
ikkje falsifisert avkvifor P5 — den er redusert til dose-respons.
