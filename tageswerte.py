from typing import Any
import json, glob
from datetime import date

MIN_MESSWERTE = 90


def main() -> None:
    records = read_zaehler_records()
    tageswerte = build_tageswerte(records)

    write_formated_json_file(tageswerte, "tageswerte.json")
    print(len(tageswerte))


def read_zaehler_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for file_path in sorted(glob.glob("data/zaehler_data_*.json")):
        with open(file_path) as data_file:
            records.extend(json.load(data_file))

    return records


def build_tageswerte(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tage: dict[str, dict[str, int]] = {}

    for record in records:
        datum = record["DATUM"][:10]
        if datum not in tage:
            tage[datum] = {"velos": 0, "messwerte": 0}

        tage[datum]["velos"] = tage[datum]["velos"] + (record["VELO_IN"] or 0) + (record["VELO_OUT"] or 0)
        tage[datum]["messwerte"] = tage[datum]["messwerte"] + 1

    tageswerte: list[dict[str, Any]] = []
    for datum in sorted(tage):
        tageswert = make_tageswert(datum, tage[datum])
        if tageswert is not None:
            tageswerte.append(tageswert)

    return tageswerte


def make_tageswert(datum: str, values: dict[str, int]) -> dict[str, Any] | None:
    if values["messwerte"] < MIN_MESSWERTE:
        return None

    weekday = date.fromisoformat(datum).weekday()
    gruppe: str = "Werktag"
    if weekday >= 5:
        gruppe = "Wochenende"

    return {
        "datum": datum,
        "velos": values["velos"],
        "messwerte": values["messwerte"],
        "gruppe": gruppe,
    }


def write_formated_json_file(data: Any, file_name: str) -> None:
    data_encoded = json.dumps(data, indent=4)

    with open(f"data/{file_name}", "w") as data_file:
        data_file.write(data_encoded)


if __name__ == "__main__":
    main()
