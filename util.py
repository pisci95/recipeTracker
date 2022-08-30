import recipe
from flask import url_for
import ingredients
import json
import os


def loadRecipe(recipe_fn):
    if recipe_fn.endswith(".json"):
        recipe_fn = recipe_fn.split(".json")[0]
    with open(f"recipes/{recipe_fn}.json", "r") as f:
        recipeJson = json.load(f)
    return recipe.Recipe(recipeJson)


def loadAllRecipes():
    files = os.listdir("recipes")
    recipeMap = {}
    for fn in files:
        recipeMap[fn] = loadRecipe(fn)
    return recipeMap


def htmlStarter(lines: list = None):
    style_file = url_for("static", filename="style.css")
    res = ""
    res += "<!DOCTYPE html>\n"
    res += "<html lang=\"en\">\n"
    res += "<head>\n"
    res += f"<link rel=\"stylesheet\" href=\"{style_file}\">"
    if lines is not None:
        for line in lines:
            res += line

    res += "</head>\n"
    return res


def htmlBottomNavBar(index=-1):
    main_pages = [
        ("/", "Home"),
        ("/create-list", "List Maker"),
        ("/test", "Update Pantry"),
    ]

    res = '<div class="navbar">'
    for i in range(len(main_pages)):
        active = 'class="active"' if index == i else ""
        link, label = main_pages[i]
        res += f"<a href=\"{link}\" {active}>{label}</a>"
    res += "</div>"
    return res






