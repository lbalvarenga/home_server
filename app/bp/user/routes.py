from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import User, Message
from datetime import datetime

from . import user
from .forms import EditForm, MessageForm, ClearMessageForm

# Log last_seen
@user.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Edit page
@user.route("/edit/", methods=("GET", "POST"))
@login_required
def edit():
    edit_form = EditForm()
    user = User.query.filter_by(username=current_user.username).first()

    if edit_form.validate_on_submit():
        if user.check_password(edit_form.password.data):
            if edit_form.edit_delete_user_confirm.data:
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for("auth.logout"))
            for key, value in edit_form.data.items():
                if key == "new_password":
                    if value:
                        user.set_password(value)
                if hasattr(User, key):
                    if value:
                        setattr(user, key, value)

            db.session.commit()
        return redirect(url_for("user.u", username=current_user.username))

    return render_template("edit.html", edit_form=edit_form, user=current_user)

# Home page
@user.route("/home/")
@login_required
def home():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    return render_template("home.html")

# Follow <username>
@user.route("/f/<username>/")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user or user is current_user:
        return redirect(url_for("user.u", username=username))

    current_user.follow(user)
    db.session.commit()

    return redirect(request.referrer)

# Unfollow <username>
@user.route("/uf/<username>/")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user or user is current_user:
        return redirect(url_for("user.u", username=username))

    current_user.unfollow(user)
    db.session.commit()

    return redirect(request.referrer)

# Users browser
@user.route("/users/browse/")
@login_required
def browse():
    users = User.query.all()
    return render_template("browse.html", users=users)

# User page
@user.route("/u/<username>/", methods=("GET", "POST"))
@login_required
def u(username):
    messages = None
    message_form = MessageForm()
    clear_message_form = ClearMessageForm()
    user = User.query.filter_by(username=username).first_or_404()
    current_user.message_sent = False

    if user != current_user:
        if message_form.validate_on_submit():
            message = Message(author=current_user,
            recipient=user,
            subject=message_form.message_subject.data,
            body=message_form.message_textarea.data
            )
            db.session.add(message)
            db.session.commit()
            current_user.message_sent = True
    
    if user == current_user:
        ### NOT IMPLEMENTED ON PAGE ###
        if clear_message_form.validate_on_submit():
            print(clear_message_form.message_id.data)
            message = Message.query.filter_by(id=clear_message_form.message_id.data).first()
            db.session.delete(message)
            db.session.commit()

        messages = current_user.messages_received.order_by(Message.timestamp.desc())

    return render_template("user.html", user=user, message_form=message_form, clear_message_form=clear_message_form, messages=messages)