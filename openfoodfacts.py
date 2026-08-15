import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"


def fetch_by_barcode(barcode):
    response = requests.get(f"{BASE_URL}/{barcode}.json")
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
