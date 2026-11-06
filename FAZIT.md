# Fazit – Data Detectives (Zwischenstand)

## Auftrag
Züri-Roll GmbH will wissen: Lohnt sich eine Verleihstation am Wochenende, oder reichen die Werktage?
Wir analysieren echte Velozähl-Daten der Stadt Zürich (Open Data, CC0) und geben eine begründete Empfehlung ab.

## Datenbasis
- **Zählstelle: 5002 – Mythenquai** (Seeufer, Innenstadt ↔ Wollishofen), `velo=1`, `status=aktuell`
- Geräte-Historie: id 6 (2010–2018, Kf 1.2) · id 3919 (2018/19) · id 5002 (2022–heute, Kf 0.98)
- **4'441 Tageswerte** (2010-07-15 bis 2026-10-12), gefiltert: Tage mit < 90 von 96 Viertelstunden gelten als unvollständig und sind entfernt
- Absent, nicht 0: 2009 und 2020–2021 war der Sensor ausgeschaltet → keine erfundenen Tage
- 2019–2022 nur rudimentär (Gerätewechsel, 2019 Jan–Feb fehlt komplett)
- Hauptanalyse-Block: **2023–2026** (985 Werktage, 395 Wochenendtage, ein Gerät, eine Kalibrierung)

## Kernbeobachtungen (aus den Grafiken, 2023–2026)
- Werktag: Median ≈ 1'650 Velos/Tag, Box ≈ 1'080–2'620
- Wochenende: Median ≈ 1'180 Velos/Tag, Box ≈ 580–2'500 → **Wochenende ≈ 70 % vom Werktag (Median)**
- Beide Verteilungen rechtsschief → Median ist die stabilere Kennzahl
- 1 extremer Wochenend-Ausreisser (≈ 6'040 Velos) + einige Werktag-Ausreisser (Sommer, Seepromenade)
- Langfristig: Ø Velos/Tag stieg von ~1'190 (2011) auf ~2'390 (2026) – der Standort wächst stetig

## Grafiken (Ordner `grafiken/`)
| Datei | Inhalt |
|---|---|
| `boxplot.png` | Kastengrafik Werktag vs Wochenende, gleiche Skala |
| `histogramm_werktag.png` / `histogramm_wochenende.png` | je Gruppe, 24 Bins, gleiche x-Skala |
| `histogramm_vergleich.png` | beide Gruppen überlagert |
| `linie_alle_jahre.png` | alle Tage 2010–2026, Messlücke als Leerraum |
| `jahresmittel.png` | Ø Velos/Tag je Jahr (Teiljahre 2010/2022 beachten) |

## Pipeline (Python statt Excel, bewilligt)
1. `main.py` – API-Fetch (CKAN datastore + CSV-Fallback), pro Jahr eine `zaehler_data_<jahr>.json`
2. `tageswerte.py` – Tageswerte bilden, <90-Messwerte-Filter, Werktag/Wochenende-Flag
3. `grafiken.py` – oben genannte Grafiken

## Unsicherheiten
- Zähler misst **Vorbeifahrende**, nicht Mietvelo-Bedarf – Proxy
- Gerätewechsel mit unterschiedlichen Korrekturfaktoren (1.2 vs 0.98)
- Wetter/Ferien nicht im Modell; 2010 und 2022 sind Teiljahre; 2026 läuft erst bis Oktober

## Offen / nächste Schritte
- [ ] `kennzahlen.py`: alle Lag- und Streumasse von Hand (Validierung gegen Trainings-Sollwerte)
- [ ] Ausreisser identifizieren (Datum + Wettercheck) und drinlassen/entfernen begründen
- [ ] Empfehlung an Züri-Roll: klare Aussage, ≥ 3 Kennzahlen, 1 benannte Unsicherheit
- [ ] Lehrperson: Zeitraum 2023–2026 + Python-Abgabe bestätigen lassen
