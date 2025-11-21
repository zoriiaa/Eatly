from app import create_app
from models import *
import json

def import_data():
    app = create_app()
    with app.app_context():

        with open("seed.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        db.session.execute(recipeIngredients_table.delete())
        Recipe.query.delete()
        IngredientList.query.delete()
        db.session.commit()

        ingredients_map = {}
        for ing in data["ingredient_list"]:
            item = IngredientList(
                id=ing["id"],
                name=ing["name"]
            )
            db.session.add(item)
            ingredients_map[ing["id"]] = item

        db.session.commit()

        recipes_map = {}
        for rec in data["recipes"]:
            recipe = Recipe(
                id=rec["id"],
                name=rec["name"],
                ingredients=rec["ingredients"],
                instructions=rec["instructions"],
                calories=rec["calories"],
                proteins=rec["proteins"],
                fats=rec["fats"],
                carbs=rec["carbs"],
                image=rec["image"]
            )
            db.session.add(recipe)
            recipes_map[rec["id"]] = recipe

        db.session.commit()

        for rel in data["recipe_ingredients"]:
            recipe_id = rel["recipe_id"]
            ingredient_id = rel["ingredient_id"]

            recipe = recipes_map.get(recipe_id)
            ingredient = ingredients_map.get(ingredient_id)

            if recipe and ingredient:
                recipe.recipe_ingredients.append(ingredient)

        db.session.commit()

if __name__ == "__main__":
    import_data()
