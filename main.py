import json
import typing
import ingredients
import recipe
from functools import reduce
import argparse
import os, sys

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--recipe', '-r', type=argparse.FileType('r'),
                    help='an integer for the accumulator')
    parser.add_argument('--test', "-t", action='store_true',
                    help='sum the integers (default: find the max)')
    parser.add_argument('--list', "-l", type=argparse.FileType('r'), nargs="+", default=[],
                        help='list or recipes to create into a shopping list')

    args = parser.parse_args()
    if args.test:
        test()
    if args.recipe is not None:
        recipeJson = json.load(args.recipe)
        print("-"*80)
        print(recipe.Recipe(recipeJson))
        print("-"*80)
    if len(args.list) > 0:
        recipeList = [recipe.Recipe(json.load(each)) for each in args.list]
        shoppingList = list(makeIngredientListFromRecipes(recipeList).values())
        for each in shoppingList:
            print(each)



def makeIngredientListFromRecipes(recipes: typing.List[recipe.Recipe]):
    ingredientDicts: typing.List[typing.Dict[str, ingredients.Ingredient]] = \
        [each.getIngredientDict() for each in recipes]
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
