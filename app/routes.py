from flask import render_template, redirect, url_for
from app import app

@app.route("/")
@app.route("/index/")
def index():
    return redirect(url_for("auth.login"))

@app.route("/about/")
def about():
    return render_template("about.html")

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html")

@app.errorhandler(500)
def internal(error):
    return render_template("errors/500.html")