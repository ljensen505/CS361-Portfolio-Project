"""
Written by Lucas Jensen
Portfolio Project for CS361
The main logic behind a recipe
"""

import json
from pprint import pprint

JSON_FILE = "recipes/recipes.json"


class RecipeBook:
    """
    Represents a recipe book containing several bread recipes
    """
    def __init__(self):
        self._recipes = {}  # a dictionary of recipe objects, ID as key
        self._id = 0
        self.__build_recipes()

    def __build_recipes(self):
        """
        Builds the recipe book from an existing json file
        :return:
        """
        with open(JSON_FILE, 'rt') as f:
            recipes_dict = json.load(f)

        for _id in recipes_dict:
            recipe_dict = recipes_dict[_id]
            recipe = Recipe(recipe_dict['name'], recipe_dict['quantity'])
            recipe.set_id(_id)
            ingredients = recipe_dict['ingredients']
            for ingredient in ingredients:
                recipe.add_ingredient(ingredient, ingredients[ingredient])
                recipe.add_ingredient(ingredient, ingredients[ingredient])
            self._recipes[_id] = recipe

    def get_recipes(self):
        return self._recipes

    def find_by_id(self, _id: int) -> object:
        """
        Finds a recipe object by its assigned id
        :param _id: int, the id of the recipe
        :return: recipe object
        """
        return self._recipes[str(_id)]

    def find_and_delete(self, _id):
        """
        Finds a recipe using its ID and deletes it
        :param _id: int of the recipe's ID
        :return: nothing
        """
        del self._recipes[str(_id)]

        # remove from JSON file
        with open(JSON_FILE, 'rt') as f:
            json_file = json.load(f)

        pprint(json_file)

        del json_file[str(_id)]

        with open(JSON_FILE, 'wt') as f:
            json.dump(json_file, f, indent=4)

    def add_recipe(self, recipe):
        """
        appends a recipe object to the recipe book
        :param recipe: recipe object
        :return: the id of the newly stored recipe
        """
        with open(JSON_FILE, 'rt') as f:
            keys = json.load(f)

        while str(self._id) in keys:
            self._id += 1

        recipe.set_id(self._id)
        saved_id = self._id
        self._recipes[str(self._id)] = recipe
        self._id += 1
        # pprint(self._recipes)
        self.save(recipe)

        return saved_id

    @staticmethod
    def save(recipe):
        """
        appends a recipe dictionary to the JSON file
        :param recipe:
        :return:
        """
        with open(JSON_FILE, 'rt') as f:
            recipe_dict = json.load(f)

        recipe_dict[recipe.get_id()] = recipe.get_recipe()

        with open(JSON_FILE, 'wt') as f:
            json.dump(recipe_dict, f, indent=4)


class Recipe:
    """
    Represents a bread recipe
    """
    def __init__(self, name: str, num_loaves: int):
        self._name = name
        self._num_loaves = num_loaves
        self._ingredients = {}
        self._id = None

    def get_recipe(self) -> dict:
        """
        builds and returns the whole recipe as a single dictionary
        :return: dictionary
        """
        recipe_dict = {
            'quantity': self._num_loaves,
            'name': self._name,
            # 'id': self._id,
            'ingredients': {}
        }

        for ingredient in self._ingredients:
            recipe_dict['ingredients'][ingredient] = self._ingredients[ingredient]

        return recipe_dict

    def get_name(self) -> str:
        return self._name

    def get_num_loaves(self) -> int:
        return self._num_loaves

    def get_ingredients(self) -> dict:
        return self._ingredients

    def get_id(self) -> int:
        return self._id

    def set_id(self, _id):
        self._id = _id

    def add_ingredient(self, name: str, mass: int) -> None:
        """
        Adds an ingredient to the recipe. Mass in grams.
        :param name: string, the name of the ingredient
        :param mass: int, the mass of the ingredient, in grams
        :return:
        """
        self._ingredients[name] = mass

    def scale(self, new_num) -> object:
        """
        Scales the recipe by a given factor
        :param new_num: integer, the number of desired loaves
        :return: Recipe object, now scaled
        """
        scale = int(new_num) / int(self._num_loaves)

        scaled_recipe = Recipe(f"{self._name} * {scale}", new_num)

        for ingredient in self._ingredients:
            mass = self._ingredients[ingredient] * scale
            scaled_recipe.add_ingredient(ingredient, round(mass))

        return scaled_recipe


def default_recipes():
    """Adds some sample data"""
    recipe_1 = Recipe('Country Brown', 1)
    recipe_2 = Recipe('Conventional White', 2)

    sample_recipes = [recipe_1, recipe_2]
    flour = 500
    water = 300
    salt = 12

    for recipe in sample_recipes:
        recipe.add_ingredient("AP Flour", flour)
        flour += 500
        recipe.add_ingredient("Water", water)
        water += 300
        recipe.add_ingredient("salt", salt)
        salt += 12

    recipe_3 = recipe_2.scale(4)

    sample_recipes.append(recipe_3)

    return sample_recipes


if __name__ == "__main__":
    recipes = default_recipes()
    book = RecipeBook()
    for recipe in recipes:
        book.add_recipe(recipe)
