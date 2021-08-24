from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
# from dotenv import load_dotenv
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, ToDoItem
from forms import RegisterForm, LoginForm, TODOItemForm
import requests
import os

app = Flask(__name__)

# load_dotenv()

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPTCHA_PRIVATE_KEY")

Bootstrap(app)
ckeditor = CKEditor(app)

# Database Connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///todolist.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("dashboard.html", current_user=current_user)
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # # Email Validation
        # response = requests.get("https://isitarealemail.com/api/email/validate", params={"email": form.email.data})
        # status = response.json()["status"]
        if User.query.filter_by(email=form.email.data).first():
            flash("You,ve already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        # elif not status == "valid":
        #     flash("Please enter a valid email address.")
        #     return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return render_template("dashboard.html", current_user=current_user)
    return render_template("register.html", form=form, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return render_template("dashboard.html", current_user=current_user)
    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", current_user=current_user)


@app.route("/add-item", methods=["GET", "POST"])
@login_required
def add_new_item():
    form = TODOItemForm()
    if form.validate_on_submit():
        if form.cancel.data:
            return render_template("dashboard.html", current_user=current_user)
        item_title = form.title.data
        item_description = form.description.data
        new_item = ToDoItem(
            title=item_title,
            description=item_description,
            author=current_user
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("dashboard", current_user=current_user))
    return render_template("add-item.html", form=form, current_user=current_user)


@app.route("/delete-item/<int:item_id>")
@login_required
def delete_item(item_id):
    item_to_delete = ToDoItem.query.get_or_404(item_id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
    except:
        pass
    return render_template("dashboard.html", current_user=current_user)


@app.route("/complete-item/<int:item_id>")
@login_required
def complete_item(item_id):
    completed_item = ToDoItem.query.get_or_404(item_id)
    completed_item.is_completed = True
    db.session.commit()
    return render_template("dashboard.html", current_user=current_user)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
