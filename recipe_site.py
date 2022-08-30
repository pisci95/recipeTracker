from flask import Flask, url_for
from main import *
import util

app = Flask(__name__)


@app.route("/")
def main_view():
    res = util.htmlStarter()
    res += "<h1>Recipes</h1>"
    recipeMap = util.loadAllRecipes()
    res += "<ul>"
    for k, v in recipeMap.items():
        recipe_fn_base = k.split(".json")[0]
        recipe_name = v.name
        res += f"<li><a href=\"/recipe/{recipe_fn_base}\">{recipe_name}</a></li>"
    res += "</ul>"
    res += util.htmlBottomNavBar(index=0)
    return res


@app.route("/recipe/<recipe_fn_base>")
def recipe_view(recipe_fn_base):
    recipeObj = util.loadRecipe(recipe_fn_base)
    name = recipeObj.name
    res = util.htmlStarter()
    res += f"<h1>{name}</h1>"
    res += "<h4>Ingrediants</h4>"
    res += "<div><ul>"
    for each in recipeObj.ingredients.values():
        res += "<li>{}</li>".format(str(each))
    res += "</ul>"

    res += "<h4>Instructions</h4>"
    res += "<ol>"
    for each in recipeObj.instructions:
        res += "<li>{}</li>".format(str(each))
    res += "</ol></div>"
    res += util.htmlBottomNavBar()
    return res


@app.route("/create-list")
def list_maker():
    recipeMap = util.loadAllRecipes()
    res = util.htmlStarter()
    res += """<div style="width: 100%;">
        <div style="float:left; width: 80%">
        Test Left
        </div>
        <div style="float:right;">
        Test Right
        </div>
    </div>
    <div style="clear:both"></div>
    """
    res += util.htmlBottomNavBar(index=1)
    return res


@app.route("/test")
def test():
    recipeMap = util.loadAllRecipes()
    res = util.htmlStarter()
    res += """<div style="width: 100%;">
        <div style="float:left; width: 80%">
    """
    res += url_for("static", filename="style.css")

    res += """
        </div>
        <div style="float:right;">
        Test Right
        </div>
    </div>
    <div style="clear:both"></div>
    """
    res += util.htmlBottomNavBar(index=2)
    return res


