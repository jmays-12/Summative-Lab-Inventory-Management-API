import pytest
from unittest.mock import patch
from app import app
from data.inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    # reset to known state before each test
    inventory.clear()
    inventory.extend([
        {
            "id": 1,
            "barcode": "0049000028911",
            "product_name": "Diet Coke Soft Drink",
            "brands": "Coke",
            "quantity": 10,
            "price": 1.99
        },
        {
            "id": 2,
            "barcode": "016000275270",
            "product_name": "Honey Nut Cheerios",
            "brands": "General Mills",
            "quantity": 24,
            "price": 5.49
        }
    ])


# GET /inventory
def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_get_all_items_search(client):
    response = client.get("/inventory?search=coke")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["product_name"] == "Diet Coke Soft Drink"


# GET /inventory/<id>
def test_get_single_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Diet Coke Soft Drink"


def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


# POST /inventory
def test_create_item_with_barcode(client):
    mock_product = {
        "barcode": "0028400090179",
        "product_name": "Cheddar & Sour Cream",
        "brands": "Ruffles",
        "ingredients_text": "Potatoes, vegetable oil..."
    }
    with patch("app.fetch_by_barcode", return_value=mock_product):
        response = client.post("/inventory", json={
            "barcode": "0028400090179",
            "quantity": 15,
            "price": 3.49
        })
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Cheddar & Sour Cream"
    assert data["quantity"] == 15


def test_create_item_barcode_not_found(client):
    with patch("app.fetch_by_barcode", return_value=None):
        response = client.post("/inventory", json={
            "barcode": "0000000000000",
            "quantity": 10,
            "price": 1.99
        })
    assert response.status_code == 404


def test_create_item_no_data(client):
    response = client.post("/inventory", json={})
    assert response.status_code == 400


# PATCH /inventory/<id>
def test_update_item(client):
    response = client.patch(
        "/inventory/1", json={"quantity": 99, "price": 2.50})
    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 99
    assert data["price"] == 2.50


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"quantity": 5})
    assert response.status_code == 404


def test_update_item_ignores_id(client):
    response = client.patch("/inventory/1", json={"id": 999, "quantity": 5})
    assert response.get_json()["id"] == 1


# DELETE /inventory/<id>
def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.get_json(
    )["item"]["product_name"] == "Diet Coke Soft Drink"
    assert len(inventory) == 1


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


# OpenFoodFacts integration
def test_fetch_by_barcode_success():
    from openfoodfacts import fetch_by_barcode
    mock_response = {
        "status": 1,
        "product": {
            "product_name": "Diet Coke",
            "brands": "Coke",
            "ingredients_text": "Carbonated water..."
        }
    }
    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        result = fetch_by_barcode("0049000028911")
    assert result["product_name"] == "Diet Coke"
    assert result["barcode"] == "0049000028911"


def test_fetch_by_barcode_not_found():
    from openfoodfacts import fetch_by_barcode
    with patch("openfoodfacts.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        result = fetch_by_barcode("0000000000000")
    assert result is None
