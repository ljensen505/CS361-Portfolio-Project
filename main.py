"""
Portfolio Project for CS361 Spring 2022
Written by Lucas Jensen
Last updated 5/12 for Assignment 1
"""
from flask import Flask, redirect, render_template, request, send_file
from recipe import Recipe, RecipeBook
from time import sleep

app = Flask(__name__)
book = RecipeBook()

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/recipes', methods=['GET'])
def recipes_page():
    recipes = book.get_recipes()
    # recipes is a dictionary of recipe objects
    if recipes == {}:
        return render_template("empty.html")
    return render_template("recipes.html", content=recipes)


@app.route('/recipes/<_id>', methods=['GET', 'POST'])
def recipe_page(_id):
    recipe = book.find_by_id(str(_id))

    if request.method == 'POST':
        if 'scale' in request.form:
            scale = request.form.get('scale')
            new = recipe.scale(scale)
            new_id = book.add_recipe(new)
            return redirect(f'/recipes/{new_id}')

        else:
            path = write_txt(_id)
            sleep(0.5)
            return send_file(path, as_attachment=True)

    return render_template("recipe.html", content=recipe, _id=_id)


def write_txt(_id):
    """
    writes to the txt file to have the microservice make a selected pdf
    :return:
    """
    print(_id)
    with open('recipe.txt', 'w') as txt_file:
        txt_file.write(_id)

    return f"recipe{_id}.pdf"


# app.route('/recipes/<id>/download')
# def


@app.route('/recipes/<_id>/delete')
def delete_recipe(_id):
    book.find_and_delete(_id)
    return redirect("/recipes")


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == "POST":
        new_recipe = Recipe(request.form.get('name'), request.form.get('yield'))
        for item in request.form:
            if item not in ['name', 'yield']:
                new_recipe.add_ingredient(item, int(request.form.get(item)))

        book.add_recipe(new_recipe)

        return redirect("/recipes")
    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=False)
