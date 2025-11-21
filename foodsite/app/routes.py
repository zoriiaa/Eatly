from app import app, db, login_manager
from app.models import User
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, redirect, url_for, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
from auth.UserLogin import UserLogin

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return UserLogin(user)
    return None

@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/profile/<name>")
@login_required
def profile(name):
    return render_template('ration.html', username=username)


@app.route("/profile/<name>/favorite")
@login_required
def favorite(name):
    return render_template('favorites.html', username=username)


@app.route("/profile/<name>/settings")
@login_required
def settings(name):
    return render_template('settings.html', username=username)

@app.route("/recipes")
@login_required
def recipes():
    return render_template('findRecipes.html')


@app.route("/recipes/recipe_details")
@login_required
def recipe_details():
    return render_template('recipeDetalis.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
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
                name=name,
                email=email
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
