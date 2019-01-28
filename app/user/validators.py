from app import db
from app.models import User
from wtforms.validators import HostnameValidation, ValidationError
from flask_login import current_user
import re


class ExistsInDb(object):
    def __init__(self, queryItem, message=None):
        self.message = message
        self.queryItem = queryItem

    def __call__(self, form, field):
        if not field.data:
            return
        for key, value in form.data.items():
            if hasattr(User, key):
                if key == self.queryItem:
                    kwargs = {self.queryItem: field.data}
                    user = User.query.filter_by(**kwargs).first()
        if user:
            raise ValidationError(self.message)


class NotExistsInDb(object):
    def __init__(self, queryItem, message=None):
        self.message = message
        self.queryItem = queryItem

    def __call__(self, form, field):
        if not field.data:
            return
        for key, value in form.data.items():
            if hasattr(User, key):
                if key == self.queryItem:
                    kwargs = {self.queryItem: field.data}
                    user = User.query.filter_by(**kwargs).first()
        if not user:
            raise ValidationError(self.message)


class CheckPassword(object):
    def __init__(self, message=None, message_no_data=None):
        self.message = message
        self.message_no_data = message_no_data

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message_no_data)
        if hasattr(form, "username") and hasattr(form, "password"):
            username = getattr(form, "username")
            password = getattr(form, "password")
            user = User.query.filter_by(username=current_user.username).first()
            if not user:
                user = User.query.filter_by(username=username.data)
            if user:
                if not user.check_password(password.data):
                    raise ValidationError(self.message)


class BetterEmail(object):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',
        re.IGNORECASE)

    def __init__(self, message=None):
        self.message = message
        self.validate_hostname = HostnameValidation(
            require_tld=True,
        )

    def __call__(self, form, field):
        value = field.data

        message = self.message
        if message is None:
            message = field.gettext('Invalid email address.')

        if not value:
            return
        if '@' not in value:
            raise ValidationError(message)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(message)

        if not self.validate_hostname(domain_part):
            raise ValidationError(message)