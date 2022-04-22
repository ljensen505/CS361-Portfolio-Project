"""
Portfolio Project for CS361 Spring 2022
Written by Lucas Jensen
Last updated 3/29/22 for Assignment 1
"""
import json
from flask import Flask, redirect, flash, render_template, request, jsonify
from markupsafe import escape

from recipe import Recipe, RecipeBook, open_json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/recipes', methods=['GET'])
def ReturnJSON():
    return render_template("recipe.html", content=open_json())


@app.route('/recipes/<_id>', methods=['GET'])
def recipe_page(_id):
    if request.method == 'GET':
        # recipe = book.find_by_id(int(_id))
        # return jsonify(recipe.get_recipe())
        recipe = open_json()[_id]
        return recipe


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

        # flash("Recipe Added!")
        return redirect("/recipes")
    return render_template("new.html")


if __name__ == "__main__":
    # testing
    # recipes = default_recipes()
    book = RecipeBook()
    # for recipe in recipes:
    #     book.add_recipes(recipe)

    app.run(debug=True)
