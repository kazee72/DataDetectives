from typing import Any
import requests, json, pandas



def main() -> None:

    zaehler_data: dict[str, Any] = get_zaehler_data()
    location_data: dict[str, Any] = get_location_data()

    write_formated_json_file(zaehler_data, "zaehler_data.json")
    write_formated_json_file(location_data, "location_data.json")



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
    pass




def match_locations(location_data: dict[str, Any], zaehler_data: dict[str, Any]) -> dict[str, Any]:
    pass



def write_formated_json_file(data, file_name):
    data_encoded = json.dumps(data, indent=4)

    with open(f"data/{file_name}", "w") as data_file:
        data_file.write(data_encoded)


if __name__ == "__main__":
    main()