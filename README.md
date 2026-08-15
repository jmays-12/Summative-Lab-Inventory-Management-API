# Python Inventory Management System

A Flask-based REST API for managing retail inventory, with OpenFoodFacts API integration and a CLI interface for employees to interact with the system.

## Technologies used

- Python
- Flask
- Pipenv
- Pytest
- [OpenFoodFacts API](https://world.openfoodfacts.org/)

## Project Structure

```
app.py                  # Flask app and route definitions
inventorymanager.py     # CRUD business logic
openfoodfacts.py        # OpenFoodFacts API integration
cli.py                  # Command-line interface
data/inventory.py       # Mock data store
tests/test_api.py       # Unit tests
```

### Testing Endpoints

All endpoints can be tested through the CLI provided, or using another custom solution. The Flask server must be running on `http://localhost:5000` before starting the CLI.

## Setup

Clone the repository and install dependencies:

```bash
pipenv install
pipenv shell
```

## Running the Application

The Flask server and CLI run in separate terminals:

```bash
# Terminal 1 - start the Flask server
python app.py

# Terminal 2 - start the CLI
python cli.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | Fetch all inventory items |
| GET | `/inventory?search=<query>` | Search items by name or brand |
| GET | `/inventory/<id>` | Fetch a single item by ID |
| POST | `/inventory` | Add a new item |
| PATCH | `/inventory/<id>` | Update an existing item |
| DELETE | `/inventory/<id>` | Remove an item |

## CLI Usage

After starting the Flask server with (`python app.py`), run `python cli.py` in a second terminal. You will be presented with a menu:

```
Inventory Manager

What would you like to do?
  1. View all items
  2. View single item
  3. Search items
  4. Add item by barcode
  5. Update item
  6. Delete item
  7. Quit
```

**Adding an item by barcode** — looks up the product on OpenFoodFacts and adds it to inventory with your provided quantity and price.

**Searching** — searches by product name or brand, e.g. typing `coke` will return any matching items.

**Updating** — select a field to update (quantity, price, product name, or brand) by item ID.

## OpenFoodFacts Integration

When adding an item by barcode, the app queries the [OpenFoodFacts API](https://world.openfoodfacts.org/) to fetch real product details including product name, brand, and ingredients. The barcode, quantity, and price are provided by the user; everything else is populated automatically.

## Testing

Run the test suite with:

```bash
pytest tests/ -v
```

Tests cover all API endpoints, search functionality, error handling, and the OpenFoodFacts integration using mocked responses.