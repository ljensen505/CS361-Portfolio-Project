"""
Written by Lucas Jensen
Portfolio Project for CS361
The main logic behind a recipe
"""
import json


class RecipeBook:
    """
    Represents a recipe book containing several bread recipes
    """
    def __init__(self):
        self._recipes = self.__build_recipes()

    @staticmethod
    def __build_recipes():
        """
        Builds the recipe book from an existing json file
        """
        with open("recipes/recipes.json", "rt") as f:
            recipes = json.load(f)

        return recipes

    def add_recipes(self, recipe: object) -> None:
        """
        Adds a recipe to the book
        :param recipe: bread recipe object
        :return: nothing
        """
        keys = open_json()
        count = 0

        while str(count) in keys:
            count += 1

        self._recipes[count] = recipe
        self.save(count, recipe)

    def get_recipes(self) -> list:
        """
        get the dict of recipes
        :return: the dict of recipes
        """
        return self._recipes

    def find_by_id(self, _id: int) -> object:
        """
        Finds a recipe object by its assigned id
        :param _id: int, the id of the recipe
        :return: recipe object
        """
        return self._recipes[_id]

    def save(self, _id: int, recipe: object) -> None:
        """
        Saves a recipe to the JSON file
        :param _id: int
        :return: nothing
        """
        self._recipes[_id] = recipe.get_recipe()

        with open("recipes/recipes.json", "wt") as f:
            json.dump(self._recipes, f, indent=4)

    def delete(self, _id: int) -> None:
        """
        Deletes a recipes as found by its ID
        :param _id: int: id of the recipe
        :return: nothing
        """
        del self._recipes[str(_id)]

        with open("recipes/recipes.json", "wt") as f:
            json.dump(self._recipes, f, indent=4)


class Recipe:
    """
    Represents a bread recipe
    """
    def __init__(self, name, num_loaves, ap_flour, water, salt):
        self._name = name
        self._num_loaves = num_loaves
        self._ingredients = {
            'ap_flour': ap_flour,
            'water': water,
            'salt': salt
        }

    def get_name(self) -> str:
        """
        Gets the name of a recipe
        :return:
        """
        return self._name

    def get_recipe(self) -> dict:
        """
        :return: returns the whole recipe as a dict, including quantity
        """
        recipe_dict = {
            'quantity': self._num_loaves,
            'name': self._name,
            'ingredients': {}
        }

        for ingredient in self._ingredients:
            recipe_dict['ingredients'][ingredient] = self._ingredients[ingredient]

        return recipe_dict

    def get_num_loaves(self) -> int:
        """
        :return: int: number of loaves the recipe calls for
        """
        return self._num_loaves

    def get_ingredients(self) -> dict:
        """
        :return: dictionary of all ingredients
        """
        return self._ingredients

    def add_ingredient(self, name: str, mass: int) -> None:
        """
        Adds an ingredient to the recipe. Mass in grams.
        :param name: string, the name of the ingredient
        :param mass: int, the mass of the ingredient, in grams
        :return:
        """
        self._ingredients[name] = mass

    def scale(self, new_num: int) -> object:
        """
        Scales the recipe by a given factor
        :param new_num: integer, the number of desired loaves
        :return: Recipe object, now scaled
        """
        scale = new_num / self._num_loaves

        ap_flour = self._ingredients['ap_flour'] * scale
        water = self._ingredients['water'] * scale
        salt = self._ingredients['salt'] * scale
        name = f"{self._name} * {scale}"

        scaled_recipe = Recipe(name, new_num, ap_flour, water, salt)

        for ingredient in self._ingredients:
            if ingredient not in ['ap_flour', 'water', 'salt']:
                mass = self._ingredients[ingredient] * scale
                scaled_recipe.add_ingredient(ingredient, mass)

        return scaled_recipe


def default_recipes():
    recipe_1 = Recipe('Country Brown', 1, 600, 300, 13)
    recipe_2 = Recipe('Conventional White', 2, 1000, 700, 25)
    recipe_3 = recipe_2.scale(4)

    return [recipe_1, recipe_2, recipe_3]


def open_json():
    """TODO"""
    with open('recipes/recipes.json') as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    recipes = default_recipes()
    book = RecipeBook()
    for recipe in recipes:
        book.add_recipes(recipe)

    # for recipe in book.get_recipes():
    #     print(book.get_recipes()[recipe])
    #
    # rec = Recipe('sandwich loaf', 2, 1000, 700, 25)
    # rec.add_ingredient('ww flour', 500)
    # rec.save('recipes.json')