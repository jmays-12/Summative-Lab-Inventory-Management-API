from flask import Flask
import requests
from .data.inventory import inventory


def get_all_items():
    if inventory:
        return inventory
    else:
        return "Inventory is empty!"


def get_item(id):
    for item in inventory:
        if item["id"] == id:
            return item

    return None


def add_item(item):
    inventory.append(item)
    return item


def update_item(id, update):
    item = get_item(id)

    if item is None:
        return None

    item.update(update)
    return item


def delete_item(id):
    item = get_item(id)

    if item is None:
        return None

    inventory.remove(item)
    return item
