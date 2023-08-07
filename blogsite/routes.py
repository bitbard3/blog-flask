from flask import render_template, url_for, flash, redirect
from blogsite.forms import LoginForm, RegistrationForm
from blogsite.models import Post, User
from blogsite import app, bcrypt, db
from flask_login import login_user
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
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successfully!", "success")
            return redirect(url_for("home_page"))
    else:
        flash("Login Unsuccessful, Please enter correct username or passowrd", "danger")
    return render_template("login.html", form=form, title="Login")
