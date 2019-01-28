from flask import render_template, redirect, url_for
from app import app

@app.route("/")
@app.route("/index/")
def index():
    return redirect(url_for("auth.login"))

@app.route("/about/")
def about():
    return render_template("about.html")