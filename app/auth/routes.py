from flask import redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from app import db
from app.models import User

from . import auth
from .forms import LoginForm, RegisterForm

# Login page
@auth.route("/login/", methods=("GET", "POST"))
def login():
    login_form =    LoginForm()
    register_form = RegisterForm()
    register_form.success = False

    if current_user.is_authenticated:
        return redirect(url_for("user.home"))

    if login_form.login_submit.data:
        if current_user.is_authenticated:
            return redirect(url_for("user.home"))
        
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user:
                if user.check_password(login_form.password.data):
                    login_user(user, remember=login_form.remember_me.data)
                    return redirect(url_for("user.home"))

    if register_form.register_submit.data:
        if current_user.is_authenticated:
            return redirect(url_for("user.home"))

        if register_form.validate_on_submit():
            new_user = User(
                username    = register_form.username.data,
                email       = register_form.email.data,
                description = register_form.description.data,
                gender      = register_form.gender.data
            )
            new_user.set_password(register_form.password.data)
            db.session.add(new_user)
            db.session.commit()
            register_form.success = True

    return render_template("login.html", login_form=login_form, register_form=register_form)

# Logout handle
@auth.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))