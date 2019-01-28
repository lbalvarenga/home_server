from app import db
from app.models import User
from wtforms.validators import HostnameValidation, ValidationError
import re


class ExistsInDb(object):
    def __init__(self, query, message=None):
        self.message = message
        self.query = query

    def __call__(self, form, field):
        if not field.data:
            return
        for key, value in form.data.items():
            if hasattr(User, key):
                if key == self.query:
                    kwargs = {self.query: field.data}
                    user = User.query.filter_by(**kwargs).first()
        if user:
            raise ValidationError(self.message)


class NotExistsInDb(object):
    def __init__(self, query, message=None):
        self.message = message
        self.query = query

    def __call__(self, form, field):
        if not field.data:
            return
        for key, value in form.data.items():
            if hasattr(User, key):
                if key == self.query:
                    kwargs = {self.query: field.data}
                    user = User.query.filter_by(**kwargs).first()
        if not user:
            raise ValidationError(self.message)


class CheckPassword(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            return
        if hasattr(form, "username") and hasattr(form, "password"):
            username = getattr(form, "username")
            password = getattr(form, "password")
            user = User.query.filter_by(username=username.data).first()
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