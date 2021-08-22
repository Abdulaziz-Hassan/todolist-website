from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
