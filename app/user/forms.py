from flask_wtf import FlaskForm
from wtforms import DateField, PasswordField, SelectField, StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Optional, Length
from .validators import ExistsInDb, CheckPassword, BetterEmail


class EditForm(FlaskForm):
    username                 = StringField("New Username", validators=[
        ExistsInDb(queryItem="username",message="Username already in use.")
    ])
    password                 = PasswordField("Current Password", validators=[
        CheckPassword(
        message="Incorrect password.",
        message_no_data="Please type your current password."
        )
    ])
    new_password             = PasswordField("New Password", validators=[
        EqualTo("new_password_confirm", message="Passwords don't match.")
    ])
    new_password_confirm     = PasswordField("Confirm Password")
    email                    = StringField("New Email", validators=[
        ExistsInDb(queryItem="username", message="Email already in use."),
        BetterEmail("Not a valid email.")
    ])
    birthday                 = DateField("Birthday", validators=[Optional()])
    description              = StringField("New Description")
    gender                   = SelectField("Gender", choices=[
        ('', "No change"),
        ('m', "Male"),
        ('f', "Female"),
        ('u', "Unspecified")],
        validators=[Optional()]
    )
    edit_submit              = SubmitField("Save Profile")
    edit_delete_user_confirm = SubmitField("Continue")


class MessageForm(FlaskForm):
    message_textarea = TextAreaField("", validators=[
        DataRequired(),
        Length(min=0, max=128)
    ])
    message_subject  = StringField("", validators=[DataRequired()])
    message_submit   = SubmitField("Send")


class ClearMessageForm(FlaskForm):
     message_id = HiddenField("test")