# This file handles unit conversions
# imperial to metric and sizes
import json
import typing
from enum import Enum

VOLUME = ["FLOZ", "FLUIDOUNCE", "TSP", "TEASPOON", "TBSP", "TABLESPOON", "C", "CUP", "PT", "PINT", "QT", "QUART", "GAL",
          "GALLON", "ML"]
DRY_VOLUME = []
WEIGHT = ["OZ", "OUNCE", "LB", "POUND", "G", "GRAM", "KG", "KILOGRAM"]
QUANTITY = ["ITEM"]


class Measurements(Enum):
    Volume = 1
    Weight = 2
    Quantity = 3
    DryVolume = 4  # maybe

    @staticmethod
    def classify(unit: str):
        unit = sanitzeUnit(unit)
        if unit in VOLUME:
            return Measurements.Volume
        if unit in WEIGHT:
            return Measurements.Quantity
        return Measurements.Quantity


class Ingredient:
    def __init__(self, recipeDict: dict):
        self.name = recipeDict["name"]
        self.amount = recipeDict["amount"]
        self.unit = recipeDict["unit"]
        self.notes = recipeDict["notes"] if "notes" in recipeDict else None
        self.unit_type = Measurements.classify(self.unit)

    @staticmethod
    def createFromArgs(name: str, amount: float, unit: str, notes: str = None):
        return Ingredient({"name": name, "amount": amount, "unit": unit, "notes": notes})

    def __str__(self):
        res = f"{self.amount} {self.unit} {self.name}"
        if self.notes is not None and len(self.notes) > 0:
            res += f", {self.notes}"
        return res

    def __add__(self, other):
        if not isinstance(other, Ingredient) or self.unit_type != other.unit_type:
            raise Exception("Couldn't combine these 2:\n\t-{}\n\t-{}".format(self, other))
        if self.unit_type == Measurements.Volume:
            amount = convertToFlOz(self.amount, self.unit) + convertToFlOz(other.amount, self.unit)
            unit = "fl. oz."
        elif self.unit_type == Measurements.Weight:
            amount = convertToLb(self.amount, self.unit) + convertToLb(other.amount, self.unit)
            unit = "lb"
        else:
            amount = self.amount + other.amount
            unit = self.unit
        name = self.name
        if self.notes is None and other.notes is None:
            notes = None
        elif self.notes is None:
            notes = other.notes
        elif other.notes is None:
            notes = self.notes
        else:
            notes = "{},{}".format(self.notes, other.notes)
        return Ingredient.createFromArgs(name, amount, unit, notes)

    def toJson(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "unit": self.unit,
            "notes": self.notes
        }


def sanitzeUnit(unit: str):
    unit = unit.upper().replace(".", "").replace(" ", "")
    if unit.endswith("S"):
        unit = unit[:-1]
    return unit


def convertToLb(amount: float, unit: str):
    unit = sanitzeUnit(unit)
    if unit in ["OZ", "OUNCE"]:
        return amount / 16
    if unit in ["LB", "POUND"]:
        return amount
    if unit in ["G", "GRAM"]:
        return amount / 453.6
    if unit in ["KG", "KILOGRAM"]:
        return amount * 2.205


def convertToFlOz(amount: float, unit: str):
    unit = sanitzeUnit(unit)
    if unit in ["OZ", "OUNCE", "FLOZ", "FLUIDOUNCE"]:
        return amount
    if unit in ["TSP", "TEASPOON"]:
        return amount / 6
    if unit in ["TBSP", "TABLESPOON"]:
        return amount / 3
    if unit in ["C", "CUP"]:
        return amount * 8
    if unit in ["PT", "PINT"]:
        return amount * 16
    if unit in ["QT", "QUART"]:
        return amount * 32
    if unit in ["GAL", "GALLON"]:
        return amount * 128
    if unit in ["ML"]:
        return amount / 29.5
