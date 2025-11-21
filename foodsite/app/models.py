from app import db
from sqlalchemy import Enum, func
from werkzeug.security import generate_password_hash, check_password_hash

favourites_table = db.Table(
    'favourites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', name='fk_favourites_user_id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', name='fk_favourites_recipe_id'), primary_key=True)
)

recipeIngredients_table = db.Table(
    'recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', name='fk_recipe_ingredients_recipe_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient_list.id', name='fk_recipe_ingredients_ingredient_id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    psw = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(Enum('Чоловік', 'Жінка', name='gender_variants'), nullable=True)
    goal = db.Column(Enum('Набрати вагу', 'Скинути вагу', 'Підтримувати вагу', name='goal_types', native_enum=False), nullable=True)
    goal_weight = db.Column(db.Float)

    menu = db.relationship('MenuInfo', back_populates='user', cascade='all, delete-orphan')
    favourite_recipes = db.relationship(
        'Recipe',
        secondary=favourites_table,
        back_populates='favourite_by'
    )
    def set_password(self, password):
        self.psw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw, password)

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)

    menu_items = db.relationship('MenuItems', back_populates='recipe', cascade='all, delete-orphan')
    favourite_by = db.relationship(
        'User',
        secondary=favourites_table,
        back_populates='favourite_recipes'
    )
    recipe_ingredients = db.relationship(
        'IngredientList',
        secondary=recipeIngredients_table,
        back_populates='in_recipe'
    )

class IngredientList(db.Model):
    __tablename__ = 'ingredient_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    in_recipe = db.relationship(
        'Recipe',
        secondary=recipeIngredients_table,
        back_populates='recipe_ingredients'
    )

class MenuInfo(db.Model):
    __tablename__ = 'menu_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    menu_date = db.Column(db.Date, server_default=func.now())
    total_calories = db.Column(db.Integer)
    total_proteins = db.Column(db.Integer)
    total_fats = db.Column(db.Integer)
    total_carbs = db.Column(db.Integer)

    user = db.relationship('User', back_populates='menu')
    items = db.relationship('MenuItems', back_populates='menu', cascade='all, delete-orphan')

class MenuItems(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_info.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    meal_type = db.Column(Enum('Сніданок', 'Обід', 'Вечеря', 'Перекус', name='meal_types'), nullable=False)

    menu = db.relationship('MenuInfo', back_populates='items')
    recipe = db.relationship('Recipe', back_populates='menu_items')
