from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional
from .validators import ExistsInDb, NotExistsInDb, CheckPassword, BetterEmail


class LoginForm(FlaskForm):
    username     = StringField("Username", validators=[
        DataRequired(),
        NotExistsInDb(query="username", message="User not found.")
    ])
    password     = PasswordField("Password", validators=[
        DataRequired(),
        CheckPassword(message="Incorrect password.")
    ])
    remember_me  = BooleanField("Remember Me")
    login_submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username         = StringField("Username", validators=[
        DataRequired(),
        ExistsInDb(query="username", message="Username already in use.")
    ])
    password         = PasswordField("Password", validators=[
        DataRequired(),
        EqualTo("password_confirm", message="Passwords don't match.")
    ])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    email            = StringField("Email", validators=[
        DataRequired(),
        ExistsInDb(query="email", message="Email already in use."),
        BetterEmail("Not a valid email.")
    ])
    birthday         = DateField("Birthday", validators=[Optional()])
    description      = StringField("Description")
    gender           = SelectField("Gender", choices=[
        ('x', "None"),
        ('m', "Male"),
        ('f', "Female"),
        ('u', "Unspecified")],
        validators=[DataRequired()]
    )
    register_submit  = SubmitField("Sign Up")