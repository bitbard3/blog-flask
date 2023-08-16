import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from blogsite.forms import LoginForm, RegistrationForm, UpdateAccountForm, CreatePostForm, UpdatePostForm
from blogsite.models import Post, User
from blogsite import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home_page():
    page = request.args.get('page', 1, int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template("home.html", posts=posts)


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
    output_size = (300, 300)
    i = Image.open(imgform)
    i.thumbnail(output_size)
    i.save(file_location)

    return img_name


@app.route("/account/<username>", methods=['GET'])
def account(username):
    page = request.args.get('page', 1, int)
    user = User.query.filter(User.username == username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("account.html", title="Account", posts=posts, user=user)


@app.route("/account", methods=['POST', 'GET'])
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
        redirect(url_for('account_update'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for(
        'static', filename='profile_pics/'+current_user.profile_img)
    return render_template("account_update.html", title="Account Update", img_file=img_file, form=form)


@app.route("/post/new", methods=['POST', 'GET'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Blog posted successfully!", "success")
        return redirect(url_for('home_page'))
    return render_template("create_post.html", title="New Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/update/<int:post_id>", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    form = UpdatePostForm()
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    else:
        if request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        elif form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Post updated successfully", "success")
            return redirect(url_for('home_page'))
    return render_template("update_post.html", title="Update Post", post=post, form=form)


@app.route("/post/delete/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for('home_page'))
