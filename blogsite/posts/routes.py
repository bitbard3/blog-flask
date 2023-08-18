from flask import Blueprint, flash, abort, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from blogsite import db
from blogsite.models import Post
from blogsite.posts.forms import CreatePostForm, UpdatePostForm
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['POST', 'GET'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Blog posted successfully!", "success")
        return redirect(url_for('main.home_page'))
    return render_template("create_post.html", title="New Post", form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/update/<int:post_id>", methods=['POST', 'GET'])
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
            return redirect(url_for('main.home_page'))
    return render_template("update_post.html", title="Update Post", post=post, form=form)


@posts.route("/post/delete/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for('main.home_page'))
