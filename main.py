"""
Portfolio Project for CS361 Spring 2022
Written by Lucas Jensen
Last updated 3/29/22 for Assignment 1
"""
from flask import Flask, redirect, render_template, request
from markupsafe import escape

from recipe import Recipe, RecipeBook, open_json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/recipes', methods=['GET'])
def ReturnJSON():
    recipes = open_json()
    if recipes == {}:
        return render_template("empty.html")
    return render_template("recipes.html", content=recipes)


@app.route('/recipes/<_id>', methods=['GET'])
def recipe_page(_id):
    if request.method == 'GET':
        recipe = book.find_by_id(_id)

        return render_template("recipe.html", content=recipe, _id=_id)


@app.route('/recipes/<_id>/delete')
def delete_recipe(_id):
    book.delete(_id)

    return redirect("/recipes")


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == "POST":
        flour = request.form.get("flour_weight")
        water = request.form.get("water_weight")
        salt = request.form.get("salt_weight")
        loaves = request.form.get("yield")
        name = request.form.get("name")

        new_recipe = Recipe(name, loaves, flour, water, salt)
        book.add_recipes(new_recipe)

        return redirect("/recipes")
    return render_template("new.html")


if __name__ == "__main__":
    book = RecipeBook()
    app.run(debug=True)
