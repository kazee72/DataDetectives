# 1-Minuten-Pitch – Screenrecording (ca. 145 Wörter)

Sprache: Standarddeutsch, frei sprechen (kein Ablesen – nur die Zahlen unten aufholen).
Aufnahme: VS-Code Fenster + evtl. zweiter Bildschirm mit den Grafiken; vorher einmal `python tageswerte.py` und `python grafiken.py` laufen lassen, damit die Grafiken aktuell sind.

| Zeit | Am Bildschirm | Gesprochener Text |
|---|---|---|
| 0–8 s | Terminal mit `main.py` oder der README | «Züri-Roll will wissen: Lohnt sich eine Veloverleih-Station am Wochenende, oder reichen die Werktage? Wir haben das mit echten Open-Data-Daten der Stadt Zürich geprüft.» |
| 8–20 s | `data/tageswerte.json` kurz aufklappen (erste Zeilen genügen) | «Grundlage ist die Velozählstelle 5002 am Mythenquai: über 4'400 Tageswerte seit 2010. Unvollständige Tage haben wir gefiltert und die Jahre 2023 bis 2026 genauer angeschaut – 985 Werktage, 395 Wochenende, ein Gerät, eine Kalibrierung.» |
| 20–40 s | `grafiken/boxplot.png`, dann `grafiken/histogramm_vergleich.png` | «Das Resultat: An einem Werktag fahren im Median rund 1'650 Velos, am Wochenende rund 1'180. Das Wochenende liegt also bei etwa 70 Prozent des Werktags – aber immer noch bei über 1'000 Velos pro Tag. Weil beide Verteilungen rechtsschief sind, vergleichen wir Mediane statt Durchschnitte.» |
| 40–50 s | `grafiken/jahresmittel.png` | «Langfristig wächst der Standort stetig: von rund 1'200 Velos pro Tag 2011 auf rund 2'400 heute.» |
| 50–60 s | Abschlussfolie/Editor mit den 3 Zahlen | «Unsere Empfehlung: Ja, eine Station am Wochenende lohnt sich – sie erreicht rund 70 Prozent des Werktags. Eine Unsicherheit: Der Zähler misst Vorbeifahrende, nicht den tatsächlichen Mietvelo-Bedarf.» |

## Spickzettel (während der Aufnahme neben dem Fenster)

- Zählstelle 5002 – Mythenquai, Daten CC0 Open Data
- 4'441 Tageswerte seit 2010, Filter: mindestens 90 von 96 Viertelstunden
- Analyseblock 2023–2026: 985 Werk-/395 Wochenendtage
- Median Werktag ≈ 1'650 · Wochenende ≈ 1'180 ≈ 70 %
- Wachstum: ≈ 1'200 (2011) → ≈ 2'400 (2026)
- Empfehlung + 1 Unsicherheit (Proxy: Vorbeifahrende ≠ Mietvelo-Bedarf)

## Checkliste laut Auftrag (FAZIT.md)

- [x] klare Aussage (Empfehlung am Schluss)
- [x] ≥ 3 Kennzahlen (Mediane, 70-%-Verhältnis, Wachstum)
- [x] 1 benannte Unsicherheit
