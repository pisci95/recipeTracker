import json
import typing
import ingredients
import recipe
from functools import reduce


def main():
    test()

def makeIngredientListFromRecipes(recipes: typing.List[recipe.Recipe]):
    ingredientDicts: typing.List[typing.Dict[str, ingredients.Ingredient]] = [each.getIngredientDict() for each in recipes]
    return reduce(recipe.ingredientReducer, ingredientDicts)

def test():
    with open("recipes/caramelizedOnions.json", "r") as f:
        caramelizedOnionsJson = json.load(f)
    caramelizedOnionsRecipe = recipe.Recipe(caramelizedOnionsJson)
    print(caramelizedOnionsRecipe)

    with open("recipes/blackenedTilapia.json", "r") as f2:
        tilapiaJson = json.load(f2)
    tilapiaRecipe = recipe.Recipe(tilapiaJson)
    print(tilapiaRecipe)

    print("Combined List:")
    for k,v in makeIngredientListFromRecipes([tilapiaRecipe, caramelizedOnionsRecipe]).items():
        print(v)


if __name__ == "__main__":
    main()
