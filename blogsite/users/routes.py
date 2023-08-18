from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from blogsite import db, bcrypt
from blogsite.models import User, Post
from blogsite.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPassowrdForm
from blogsite.users.utils import saveimgage, send_email
users = Blueprint('users', __name__)


@users.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
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
        return redirect(url_for('main.home_page'))
    return render_template("register.html", form=form, title="Register")


@users.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successfully!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home_page"))
        else:
            flash(
                "Login Unsuccessful, Please enter correct username or passowrd", "danger")
    return render_template("login.html", form=form, title="Login")


@users.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully! See you soon!", "success")
    return redirect(url_for("main.home_page"))


@users.route("/account/<username>", methods=['GET'])
def account(username):
    page = request.args.get('page', 1, int)
    user = User.query.filter(User.username == username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("account.html", title="Account", posts=posts, user=user)


@users.route("/account", methods=['POST', 'GET'])
@login_required
def account_update():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = saveimgage(form.image.data)
            current_user.profile_img = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        redirect(url_for('users.account_update'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for(
        'static', filename='profile_pics/'+current_user.profile_img)
    return render_template("account_update.html", title="Account Update", img_file=img_file, form=form)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for("main.home_page"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("An email has been sent to reset your password", "info")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for("main.home_page"))
    user = User.verify_token(token)
    if user is None:
        flash("The token is expired or invalid", "warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPassowrdForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password has been reset successfully! Please login", "success")
        return redirect(url_for('users.login'))
    return render_template("reset_password.html", title="Reset Password", form=form)
