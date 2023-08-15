import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from blogsite.forms import LoginForm, RegistrationForm, UpdateAccountForm
from blogsite.models import Post, User
from blogsite import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
dummy_data = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=dummy_data)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Successfully created an acccount for {form.username.data}!', "success")
        return redirect(url_for('home_page'))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successfully!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home_page"))
        else:
            flash(
                "Login Unsuccessful, Please enter correct username or passowrd", "danger")
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully! See you soon!", "success")
    return redirect(url_for("home_page"))


def saveimgage(imgform):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imgform.filename)
    img_name = random_hex + ext
    file_location = os.path.join(
        app.root_path, 'static/profile_pics', img_name)
    imgform.save(file_location)

    return img_name


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = saveimgage(form.image.data)
            current_user.profile_img = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for(
        'static', filename='profile_pics/'+current_user.profile_img)
    return render_template("account.html", title="Account", img_file=img_file, form=form)
