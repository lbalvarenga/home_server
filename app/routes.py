from flask import redirect, url_for
from app import app

@app.route("/")
@app.route("/index/")
def index():
    return redirect(url_for("auth.login"))