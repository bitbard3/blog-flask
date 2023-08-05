from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '8562f33c5ce406479b245c3fec88f9fe'
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
        flash(
            f'Successfully created an acccount for {form.username.data}!', "success")
        return redirect(url_for('home_page'))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "test@blog.com" and form.password.data == "password":
            flash("Login Successfully!", "success")
            return redirect(url_for("home_page"))
    else:
        flash("Login Unsuccessful, Please enter correct username or passowrd", "danger")
    return render_template("login.html", form=form, title="Login")


if __name__ == "__main__":
    app.run(debug=True)
