from flask import Flask, render_template, redirect, url_for, abort, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from forms import RegisterForm, LoginForm
from flask_login import login_user, LoginManager, current_user, logout_user
from database import db
from models import User, ToDoItem
import os

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPTCHA_PRIVATE_KEY")

ckeditor = CKEditor(app)
Bootstrap(app)

# Database Connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todolist.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    return render_template("todolist.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)