from app import app, db, login_manager
from app.models import User, Recipe, IngredientList, MenuInfo, MenuItems
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, redirect, url_for, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
from app.auth.UserLogin import UserLogin
from app.functions.search_recipe import search_recipes, filter_recipes_by_ingredients, calculate_calories, get_recipe_by_id

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return UserLogin(user)
    return None

@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/profile/<name>", methods = ["POST"])
@login_required
def profile(name):
    data = request.form

    weight = float(data["weight"])
    height = float(data["height"])
    age = int(data["age"])
    gender = data["gender"]
    activity =  data["activity"]
    goal = data["goal"]

    daily_calories = calculate_calories(weight, height, age, gender, activity, goal)

    return render_template('ration.html', calories=daily_calories, name=name)


@app.route("/profile/<name>/favorite")
@login_required
def favorite(name):
    return render_template('favorites.html', name=name)


@app.route("/profile/<name>/settings")
@login_required
def settings(name):
    return render_template('settings.html', name=name)

@app.route("/recipes", methods=["GET", "POST"])
@login_required
def recipes():
    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")
        ingredients_list = [i.strip() for i in ingredients.split(",")]
        recipes_list = filter_recipes_by_ingredients(ingredients_list)
        return render_template("findRecipes.html", recipes=recipes_list)

    keyword = request.args.get("keyword", "")
    recipes_list = search_recipes(keyword)
    return render_template("findRecipes.html", recipes=recipes_list)


@app.route("/recipe")
def recipe_details():
    recipe_id = request.args.get("id")

    recipe = Recipe.query.get(recipe_id)

    if recipe is None:
        return "Рецепт не знайдено", 404

    return render_template(
        "recipeDetails.html",
        name=recipe.name,
        ingredients=recipe.recipe_ingredients,
        instructions=recipe.instructions,
        calories=recipe.calories,
        proteins=recipe.proteins,
        fats=recipe.fats,
        carbs=recipe.carbs,
        image=recipe.image
    )




@app.route("/recipe_details")
@login_required
def recipe_details_view(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipeDetails.html', recipe=recipe)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        psw = request.form['psw']

        if len(name) <= 4:
            flash("Ім'я занадто коротке", "error")
        elif len(psw) <= 4:
            flash("Пароль занадто короткий", "error")
        else:
            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError as e:
                flash(f"Неправильний email: {str(e)}", "error")
                return redirect('/register')

            if User.query.filter_by(email=email).first():
                flash("Користувач з таким email вже існує!", "error")
                return redirect("/register")
            user = User(
                email=email,
                name=name
            )
            user.set_password(psw)

            db.session.add(user)
            db.session.commit()
            session["email"] = email
            flash("Реєстрація пройшла успішно!", "success")
            return redirect("/register_info")
    return render_template('registration.html')


@app.route("/register_info", methods=["POST", "GET"])
def register_info():
    email = session.get("email")
    if not email:
        flash("Помилка: не знайдено користувача", "error")
        return redirect("/register")

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Користувач не знайдений", "error")
        return redirect("/register")
    if request.method == "POST":
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        gender = request.form["gender"]
        goal_weight = float(request.form.get("goal_weight", 0))
        if not 0 < age < 100 and 20 < height < 300 and 0 < weight < 650:
            flash("Невірні параметри! Перевір введені значення.", "error")
            return redirect("/register_info")
        user.age = age
        user.height = height
        user.weight = weight
        user.goal = goal
        user.gender = gender
        user.goal_weight = goal_weight
        db.session.commit()
        flash("Профіль успішно збережено!", "success")
        return redirect("/login")
    return render_template('registrationData.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        psw = request.form['psw']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(psw):
            remember = True if request.form.get("remember") else False
            login_user(UserLogin(user), remember=remember)
            flash("Вхід успішний!", "success")
            res = make_response(redirect(url_for('profile', name=user.name)))
            res.set_cookie("logged", "yes", max_age=30 * 24 * 3600)  # 30 днів
            return res
        else:
            flash("Невірний email або пароль", "error")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з профілю", "success")
    res = make_response(redirect(url_for('login')))
    res.set_cookie("logged", "", 0)

    return res
