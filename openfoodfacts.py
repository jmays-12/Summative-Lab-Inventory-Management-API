import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2/product"

HEADERS = {
    "User-Agent": "SummativeLabInventoryManager/1.0"
}


def fetch_by_barcode(barcode):
    response = requests.get(
        f"{BASE_URL}/{barcode}",
        headers=HEADERS
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    if data["status"] != 1:
        return None

    product = data["product"]
    return {
        "barcode": barcode,
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
    }
