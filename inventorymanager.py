from data.inventory import inventory


def get_all_items():
    if inventory:
        return inventory
    return []


def get_item(id):
    for item in inventory:
        if item["id"] == id:
            return item
    return None


def search_items(query):
    query = query.lower()
    results = []
    for item in inventory:
        if query in item.get("product_name", "").lower() or query in item.get("brands", "").lower():
            results.append(item)
    return results


def add_item(data):
    item = {
        "id": max((i["id"] for i in inventory), default=0) + 1,
        "barcode": data.get("barcode", ""),
        "product_name": data.get("product_name", "Unknown"),
        "brands": data.get("brands", "Unknown"),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0)
    }
    inventory.append(item)
    return item


def update_item(id, update):
    item = get_item(id)
    if item is None:
        return None
    # only allow updating these fields
    allowed = {"product_name", "brands", "quantity", "price"}
    for key, value in update.items():
        if key in allowed:
            item[key] = value
    return item


def delete_item(id):
    item = get_item(id)
    if item is None:
        return None
    inventory.remove(item)
    return item
