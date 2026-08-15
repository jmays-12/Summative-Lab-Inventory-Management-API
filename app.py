from flask import Flask, request, jsonify
from inventorymanager import get_all_items, get_item, search_items, add_item, update_item, delete_item
from openfoodfacts import fetch_by_barcode

app = Flask(__name__)


@app.route("/inventory", methods=["GET"])
def fetch_all():
    query = request.args.get("search")
    if query:
        results = search_items(query)
        return jsonify(results)
    return jsonify(get_all_items())


@app.route("/inventory/<int:id>", methods=["GET"])
def fetch_one(id):
    item = get_item(id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    barcode = data.get("barcode")
    if barcode:
        product_data = fetch_by_barcode(barcode)
        if product_data is None:
            return jsonify({"error": "Barcode not found in OpenFoodFacts API"}), 404
        data.update(product_data)

    if not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400

    new_item = add_item(data)
    return jsonify(new_item), 201


@app.route("/inventory/<int:id>", methods=["PATCH"])
def edit_item(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    updated = update_item(id, data)
    if updated is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated)


@app.route("/inventory/<int:id>", methods=["DELETE"])
def remove_item(id):
    deleted = delete_item(id)
    if deleted is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted", "item": deleted})


if __name__ == "__main__":
    app.run(debug=True)
