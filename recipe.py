import copy
import typing
import json

from ingredients import Ingredient


def ingredientReducer(ingDictA: typing.Dict[str, Ingredient], ingDictB: typing.Dict[str, Ingredient]):
    res = copy.copy(ingDictA)
    namesA = set([name.upper() for name in ingDictA.keys()])
    for (k, v) in ingDictB.items():
        k_upper = k.upper()
        if k_upper in namesA:
            res[k] = res[k] + v
        else:
            res[k] = v
    return res


class Recipe:
    def __init__(self, recipeJson: dict):
        self.ingredients = dict()
        for each in recipeJson["ingredients"]:
            self.ingredients[each["name"]] = Ingredient(each)
        self.instructions = recipeJson["instructions"]
        self.name = recipeJson["name"]

    def __str__(self):
        res = f"{self.name}\n\n"
        res += "Ingredients:\n"
        for each in self.ingredients.values():
            res += "\t- {}\n".format(str(each))

        res += "Instructions:\n"
        i = 1
        for each in self.instructions:
            res += "\t{}. {}\n".format(i, each)
            i += 1

        return res

    def getIngredientDict(self):
        return self.ingredients

    def createNewRecipe(self):
        print("GUI TIME!!! or maybe javascript?")
