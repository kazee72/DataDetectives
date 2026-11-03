from typing import Any
import requests, json, pandas



def main() -> None:

    zaehler_data: dict[str, Any] = get_zaehler_data()
    location_data: dict[str, Any] = get_location_data()
    cleaned_location_data: dict[str, Any] = clean_location_data(location_data)

    write_formated_json_file(zaehler_data, "zaehler_data.json")
    write_formated_json_file(location_data, "location_data.json")
    write_formated_json_file(clean_location_data, "cleaned_location_data.json")

def get_zaehler_data() -> dict[str, Any]:
    url = "https://data.stadt-zuerich.ch/api/3/action/datastore_search"
    data = requests.get(url, params={
        "resource_id": "ab641c27-53c0-433d-bd02-e25394ba0918",
        "limit": 1000,
    }).json()

    return data



def get_location_data() -> dict[str, Any]:
    url = "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Standorte_der_automatischen_Fuss__und_Velozaehlungen"
    data = requests.get(url, params={
        "SERVICE": "WFS",
        "VERSION": "1.1.0", 
        "REQUEST": "GetFeature", 
        "TYPENAME": "view_eco_standorte",
        "OUTPUTFORMAT": "application/json"
    }).json()

    return data



def clean_location_data(location_data: dict[str, Any]) -> dict[str, Any]:
    cleaned_data: dict[str, Any] = {}

    locations: dict[str, Any] = location_data["features"]

    for location in locations:
        sub_dict: dict[str, str] = {}
        location_id = location["properties"]["id1"]
        location_name = location["properties"]["bezeichnung"]
        direction_in = location["properties"]["richtung_in"]
        direction_out = location["properties"]["richtung_out"]        

        sub_dict["bezeichnung"] = location_name
        sub_dict["in"] = direction_in
        sub_dict["out"] = direction_out

        cleaned_data[location_id] = sub_dict

    return cleaned_data




def match_locations(cleaned_location_data: dict[str, Any], zaehler_data: dict[str, Any]) -> dict[str, Any]:
    pass



def write_formated_json_file(data: dict[Any, Any], file_name: str) -> None:
    data_encoded = json.dumps(data, indent=4)

    with open(f"data/{file_name}", "w") as data_file:
        data_file.write(data_encoded)


if __name__ == "__main__":
    main()