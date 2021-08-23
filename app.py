from flask import Flask, render_template, redirect, url_for, abort, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from forms import RegisterForm, LoginForm
import os

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
