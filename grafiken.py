from typing import Any
import json, os
from datetime import date, timedelta
import matplotlib.pyplot as plt

ZAEHLSTELLE = "5002 - Mythenquai"
ZEITRAUM_AB = 2023
BINS = 24


def main() -> None:
    alle_tageswerte = read_tageswerte()
    tageswerte = [tageswert for tageswert in alle_tageswerte if int(tageswert["datum"][:4]) >= ZEITRAUM_AB]

    werktag, wochenende = split_nach_gruppe(tageswerte)
    skala_max = max(werktag + wochenende)

    os.makedirs("grafiken", exist_ok=True)

    build_boxplot(werktag, wochenende, skala_max)
    build_histogramm(werktag, "Werktag", skala_max)
    build_histogramm(wochenende, "Wochenende", skala_max)
    build_histogramm_vergleich(werktag, wochenende, skala_max)
    build_liniendiagramm(alle_tageswerte)
    build_jahresmittel(alle_tageswerte)

    print(len(werktag), len(wochenende), skala_max)


def read_tageswerte() -> list[dict[str, Any]]:
    with open("data/tageswerte.json") as data_file:
        return json.load(data_file)


def split_nach_gruppe(tageswerte: list[dict[str, Any]]) -> tuple[list[int], list[int]]:
    werktag: list[int] = []
    wochenende: list[int] = []

    for tageswert in tageswerte:
        if tageswert["gruppe"] == "Werktag":
            werktag.append(tageswert["velos"])
        else:
            wochenende.append(tageswert["velos"])

    return werktag, wochenende


def build_boxplot(werktag: list[int], wochenende: list[int], skala_max: int) -> None:
    plt.figure(figsize=(8, 5))
    plt.boxplot([werktag, wochenende], tick_labels=["Werktag", "Wochenende"], showfliers=True)
    plt.title(f"{ZAEHLSTELLE} - Velos pro Tag, {ZEITRAUM_AB}-2026")
    plt.ylabel("Velos pro Tag")
    plt.ylim(0, skala_max * 1.05)
    plt.grid(True, axis="y", alpha=0.3)
    plt.savefig("grafiken/boxplot.png", dpi=150, bbox_inches="tight")
    plt.close()


def build_histogramm(velos: list[int], gruppe: str, skala_max: int) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(velos, bins=BINS, range=(0, skala_max * 1.05), edgecolor="white")
    plt.title(f"{ZAEHLSTELLE} - Velos pro Tag, {ZEITRAUM_AB}-2026 ({gruppe})")
    plt.xlabel("Velos pro Tag")
    plt.ylabel("Anzahl Tage")
    plt.xlim(0, skala_max * 1.05)
    plt.savefig(f"grafiken/histogramm_{gruppe.lower()}.png", dpi=150, bbox_inches="tight")
    plt.close()


def build_histogramm_vergleich(werktag: list[int], wochenende: list[int], skala_max: int) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist([werktag, wochenende], bins=BINS, range=(0, skala_max * 1.05),
             label=["Werktag", "Wochenende"], edgecolor="white")
    plt.title(f"{ZAEHLSTELLE} - Velos pro Tag, {ZEITRAUM_AB}-2026 (Vergleich)")
    plt.xlabel("Velos pro Tag")
    plt.ylabel("Anzahl Tage")
    plt.xlim(0, skala_max * 1.05)
    plt.legend()
    plt.savefig("grafiken/histogramm_vergleich.png", dpi=150, bbox_inches="tight")
    plt.close()


def build_liniendiagramm(alle_tageswerte: list[dict[str, Any]]) -> None:
    velos_nach_datum: dict[str, int] = {}
    for tageswert in alle_tageswerte:
        velos_nach_datum[tageswert["datum"]] = tageswert["velos"]

    erster = date.fromisoformat(min(velos_nach_datum))
    letzter = date.fromisoformat(max(velos_nach_datum))
    datum = erster

    tage: list[date] = []
    werte: list[int | None] = []
    while datum <= letzter:
        tage.append(datum)
        if datum.isoformat() in velos_nach_datum:
            werte.append(velos_nach_datum[datum.isoformat()])
        else:
            werte.append(None)
        datum = datum + timedelta(days=1)

    plt.figure(figsize=(12, 5))
    plt.plot(tage, werte, linewidth=0.6)
    plt.title(f"{ZAEHLSTELLE} - Velos pro Tag, alle Jahre")
    plt.ylabel("Velos pro Tag")
    plt.grid(True, alpha=0.3)
    plt.savefig("grafiken/linie_alle_jahre.png", dpi=150, bbox_inches="tight")
    plt.close()


def build_jahresmittel(alle_tageswerte: list[dict[str, Any]]) -> None:
    summe: dict[int, int] = {}
    anzahl: dict[int, int] = {}
    for tageswert in alle_tageswerte:
        jahr = int(tageswert["datum"][:4])
        if jahr not in summe:
            summe[jahr] = 0
            anzahl[jahr] = 0
        summe[jahr] = summe[jahr] + tageswert["velos"]
        anzahl[jahr] = anzahl[jahr] + 1

    jahre: list[int] = sorted(summe)
    mittel: list[float] = []
    for jahr in jahre:
        mittel.append(summe[jahr] / anzahl[jahr])

    plt.figure(figsize=(9, 5))
    plt.bar([str(jahr) for jahr in jahre], mittel)
    plt.title(f"{ZAEHLSTELLE} - durchschnittliche Velos pro Tag je Jahr")
    plt.ylabel("Ø Velos pro Tag")
    plt.grid(True, axis="y", alpha=0.3)
    plt.savefig("grafiken/jahresmittel.png", dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
