"""
Portfolio Project for CS361 Spring 2022
Written by Lucas Jensen
Last updated 5/12 for Assignment 1
"""
from flask import Flask, redirect, render_template, request, send_file
from recipe import Recipe, RecipeBook
from werkzeug.utils import secure_filename
from time import sleep
import subprocess
import os

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


@app.route('/recipes/<_id>/email', methods=['GET', 'POST'])
def email_page(_id):
    recipe = book.find_by_id(str(_id))

    if request.method == 'POST':
        addr = request.form.get('email')
        subject = recipe.get_name()
        message = f"{subject}; " \
                  f"Num loaves: {recipe.get_num_loaves()};"
        ingredients = recipe.get_ingredients()
        for item in ingredients:
            message += f" {item}: {ingredients[item]} grams;"

        body = f"$to == {addr}\n" \
               f"$subject == {subject}\n" \
               f"$message == {message}"

        with open('mail.txt', 'wt') as txt_file:
            txt_file.write(body)

        subprocess.call(['python', 'mailer.py'])

        return redirect('/recipes')

    return render_template('email.html', content=recipe)


@app.route('/recipes/<_id>', methods=['GET', 'POST'])
def recipe_page(_id):
    recipe = book.find_by_id(_id)

    if request.method == 'POST':
        # user wants to scale their recipe
        if 'scale' in request.form:
            scale = request.form.get('scale')
            new = recipe.scale(scale)
            new_id = book.add_recipe(new)
            return redirect(f'/recipes/{new_id}')
        elif 'photo' in request.files:
            # user wants to add a photo
            f = request.files['photo']
            f.save(os.path.join('static', f"image_{_id}.jpg"))
            # return "Success"
        elif 'convert' in request.form:
            # user wants to convert to sourdough
            new_recipe = recipe.convert()
            book.add_recipe(new_recipe)
            return redirect('/recipes')
        else:
            # user wants to download a pdf
            path = write_txt(_id)
            sleep(0.5)
            return send_file(path, as_attachment=True)

    # find all associated images
    recipe_photos = []
    all_photos = os.listdir('static')
    for photo in all_photos:
        if 'jpg' in photo:
            if get_num(photo) == int(_id):
                recipe_photos.append(photo)

    return render_template("recipe.html", content=recipe, _id=_id, photos=recipe_photos)


def get_num(path: str) -> int:
    """
    :param path: must be formatted: "image_XXX.jpg" where XXX is the id of the recipe with any number of digits
    :return: integer of the found id number
    """
    num = ""
    for i in range(6, len(path)):
        if path[i] == '.':
            break
        num += path[i]

    return int(num)


def write_txt(_id):
    """
    writes to the txt file to have the microservice make a selected pdf
    :return:
    """
    print(_id)
    with open('recipe.txt', 'w') as txt_file:
        txt_file.write(_id)

    return f"recipe{_id}.pdf"


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
    app.run(debug=True)
