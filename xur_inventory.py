from enum import Enum
from constants import *
import requests
from bs4 import BeautifulSoup
import api

KEYS = ['name', 'type', 'hash', 'damageType']


class DamageType(Enum):
    """Enumeration type defining each Damage type as described in the Destiny API

    **Kinetic** = 1

    **Arc** = 2

    **Solar** = 3

    **Void** = 4

    """
    NONE = 0
    KINETIC = 1
    ARC = 2
    SOLAR = 3
    VOID = 4
    RAID = 5


class PlayerClass(Enum):  # Player class and weapon Enum for creating dictionary
    """Enumeration type defining each player class as described in the Destiny API

    **Titan** = 0

    **Hunter** = 1

    **Warlock** = 2

    **Weapon** = 3

    """

    Titan = 0
    Hunter = 1
    Warlock = 2
    Weapon = 3


def items() -> dict:
    """Retrieve Xur's inventory

    :return: dict -
        {class_type: {'name': 'item_name', 'type': 'item_type', 'hash': 'item_hash', 'damageType': 'damage_type'}}
    """
    inventory = {}
    xur_items = api.public_vendor_items(XUR_HASH)
    count = 0
    for item in xur_items:  # For each item he's selling, find it's name, type, hash and class type
        item_hash = xur_items[item]['itemHash']  # current item hash

        item_info = api.manifest(ITEM, item_hash)

        name = item_info['displayProperties']['name']  # current item name
        class_type = (PlayerClass(item_info['classType'])).name  # current item class
        item_type = item_info['itemTypeDisplayName']  # current item type
        damage_type = (DamageType(item_info['defaultDamageType'])).name
        item_dict = dict(zip(KEYS, [name, item_type, item_hash, damage_type]))  # create dictionary for current item
        inventory[class_type] = item_dict  # set key 'class type' to current dictionary inside the inventory dictionary

        if count == 3:
            break
        count += 1

    return inventory


def location() -> str:
    """Returns Xur's location

    :return: str
    """
    xur_location = []
    URL = 'https://xur.wiki/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_="location-text-container").get_text()  # Find's Xur's latest location
    xur_location.append(result.partition("This")[0].partition(" ")[2])
    xur_location.append("I am standing" + result.partition("standing")[2][:-1])
    return xur_location[1]