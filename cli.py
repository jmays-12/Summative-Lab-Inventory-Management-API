import requests

BASE_URL = "http://localhost:5000"


def view_all():
    response = requests.get(f"{BASE_URL}/inventory")
    items = response.json()
    if not items:
        print("Inventory is empty.")
        return
    for item in items:
        print(f"\n[{item['id']}] {item['product_name']} - {item['brands']}")
        print(f"    Price: ${item['price']} | Quantity: {item['quantity']}")


def view_one():
    id = input("Enter item ID: ")
    response = requests.get(f"{BASE_URL}/inventory/{id}")
    if response.status_code == 404:
        print("Item not found.")
        return
    item = response.json()
    print(f"\n[{item['id']}] {item['product_name']} - {item['brands']}")
    print(f"    Barcode: {item['barcode']}")
    print(f"    Price: ${item['price']} | Quantity: {item['quantity']}")


def search():
    query = input("Search by name or brand: ")
    response = requests.get(f"{BASE_URL}/inventory", params={"search": query})
    items = response.json()
    if not items:
        print("No results found.")
        return
    for item in items:
        print(f"\n[{item['id']}] {item['product_name']} - {item['brands']}")
        print(f"    Price: ${item['price']} | Quantity: {item['quantity']}")


def add_by_barcode():
    barcode = input("Enter barcode: ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    response = requests.post(f"{BASE_URL}/inventory", json={
        "barcode": barcode,
        "quantity": int(quantity),
        "price": float(price)
    })
    if response.status_code == 404:
        print("Barcode not found on OpenFoodFacts.")
        return
    if response.status_code == 400:
        print(f"Error: {response.json().get('error')}")
        return
    item = response.json()
    print(f"\nAdded: [{item['id']}] {item['product_name']} - {item['brands']}")


def add_manually():
    product_name = input("Product name: ")
    brands = input("Brand: ")
    barcode = input("Barcode (optional, press enter to skip): ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    response = requests.post(f"{BASE_URL}/inventory", json={
        "product_name": product_name,
        "brands": brands,
        "barcode": barcode,
        "quantity": int(quantity),
        "price": float(price)
    })
    item = response.json()
    print(f"\nAdded: [{item['id']}] {item['product_name']}")


def update():
    id = input("Enter item ID to update: ")
    print("What would you like to update?")
    print("  1. Quantity")
    print("  2. Price")
    print("  3. Product name")
    print("  4. Brand")
    choice = input("> ")

    fields = {"1": "quantity", "2": "price",
              "3": "product_name", "4": "brands"}
    if choice not in fields:
        print("Invalid choice.")
        return

    field = fields[choice]
    value = input(f"New {field}: ")

    if field == "quantity":
        value = int(value)
    elif field == "price":
        value = float(value)

    response = requests.patch(
        f"{BASE_URL}/inventory/{id}", json={field: value})
    if response.status_code == 404:
        print("Item not found.")
        return
    item = response.json()
    print(f"\nUpdated: [{item['id']}] {item['product_name']}")
    print(f"    Price: ${item['price']} | Quantity: {item['quantity']}")


def delete():
    id = input("Enter item ID to delete: ")
    confirm = input(f"Are you sure you want to delete item {id}? (y/n): ")
    if confirm.lower() != "y":
        print("Cancelled.")
        return
    response = requests.delete(f"{BASE_URL}/inventory/{id}")
    if response.status_code == 404:
        print("Item not found.")
        return
    print(f"Deleted: {response.json()['item']['product_name']}")


def main():
    print("\nInventory Manager")
    print("Make sure the Flask server is running! (Run 'python app.py' in another terminal)\n")

    options = {
        "1": ("View all items", view_all),
        "2": ("View single item", view_one),
        "3": ("Search items", search),
        "4": ("Add item by barcode", add_by_barcode),
        "5": ("Update item", update),
        "6": ("Delete item", delete),
        "7": ("Exit", None)
    }

    while True:
        print("\nWhat would you like to do?")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")

        choice = input("\n> ").strip()

        if choice == "7":
            print("Exiting...")
            break
        elif choice in options:
            options[choice][1]()
            input("\nPress enter to continue...")
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
