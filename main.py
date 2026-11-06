from typing import Any
import requests, json, csv, io

ZAEHLER_API = "https://data.stadt-zuerich.ch/api/3/action"
ZAEHLER_DATASET = "ted_taz_verkehrszaehlungen_werte_fussgaenger_velo"
MYTHENQUAI_IDS = ("6", "3919", "5002")


def main() -> None:
    location_data = get_location_data()
    cleaned_location_data = clean_location_data(location_data)

    write_formated_json_file(location_data, "location_data.json")
    write_formated_json_file(cleaned_location_data, "cleaned_location_data.json")

    resources = get_zaehler_resources()
    for year, resource in sorted(resources.items()):
        if resource["datastore_active"]:
            records = get_zaehler_data(resource["id"])
        else:
            records = get_zaehler_data_csv(resource["name"])

        cleaned_records: list[dict[str, Any]] = []
        for record in records:
            cleaned_records.append(clean_zaehler_record(record))

        write_formated_json_file(cleaned_records, f"zaehler_data_{year}.json")
        print(year, len(cleaned_records))


def get_zaehler_resources() -> dict[int, dict[str, Any]]:
    data = requests.get(f"{ZAEHLER_API}/package_show", params={"id": ZAEHLER_DATASET}, timeout=30)
    data.raise_for_status()
    body = data.json()

    resources: dict[int, dict[str, Any]] = {}
    for resource in body["result"]["resources"]:
        file_name = resource["name"]
        if file_name[:4].isdigit():
            resources[int(file_name[:4])] = resource

    return resources


def get_zaehler_data(resource_id: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    offset = 0

    while True:
        data = requests.get(f"{ZAEHLER_API}/datastore_search", params={
            "resource_id": resource_id,
            "filters": json.dumps({"FK_STANDORT": list(MYTHENQUAI_IDS)}),
            "limit": 1000,
            "offset": offset,
        }, timeout=30)
        data.raise_for_status()
        body = data.json()

        if not body["success"]:
            raise RuntimeError(f"datastore_search failed: {body['error']}")

        result = body["result"]
        for record in result["records"]:
            records.append(record)
        offset = offset + len(result["records"])

        if offset >= result["total"] or not result["records"]:
            break

    return records


def get_zaehler_data_csv(title: str) -> list[dict[str, Any]]:
    url = f"https://data.stadt-zuerich.ch/dataset/{ZAEHLER_DATASET}/download/{title}"
    data = requests.get(url, timeout=60)
    data.raise_for_status()

    records: list[dict[str, Any]] = []
    for row in csv.DictReader(io.StringIO(data.text)):
        if row["FK_STANDORT"] in MYTHENQUAI_IDS:
            records.append(row)

    return records


def clean_zaehler_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "FK_STANDORT": str(record["FK_STANDORT"]),
        "DATUM": record["DATUM"],
        "VELO_IN": to_int(record["VELO_IN"]),
        "VELO_OUT": to_int(record["VELO_OUT"]),
    }


def to_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def get_location_data() -> dict[str, Any]:
    url = "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Standorte_der_automatischen_Fuss__und_Velozaehlungen"
    data = requests.get(url, params={
        "SERVICE": "WFS",
        "VERSION": "1.1.0",
        "REQUEST": "GetFeature",
        "TYPENAME": "view_eco_standorte",
        "OUTPUTFORMAT": "application/json"
    }, timeout=30).json()

    return data


def clean_location_data(location_data: dict[str, Any]) -> dict[str, Any]:
    cleaned_data: dict[str, Any] = {}

    locations: list[dict[str, Any]] = location_data["features"]

    for location in locations:
        sub_dict: dict[str, str | None] = {}
        location_id = location["properties"]["id1"]
        location_name = location["properties"]["bezeichnung"]
        direction_in = location["properties"]["richtung_in"]
        direction_out = location["properties"]["richtung_out"]

        sub_dict["bezeichnung"] = location_name
        sub_dict["in"] = direction_in
        sub_dict["out"] = direction_out

        cleaned_data[location_id] = sub_dict

    cleaned_data_sorted: dict[str, Any] = dict(
        sorted(cleaned_data.items(), key=lambda item: int(item[0]))
    )

    return cleaned_data_sorted


def write_formated_json_file(data: Any, file_name: str) -> None:
    data_encoded = json.dumps(data, indent=4)

    with open(f"data/{file_name}", "w") as data_file:
        data_file.write(data_encoded)


if __name__ == "__main__":
    main()
