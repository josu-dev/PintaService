import typing as t

import wtforms
from flask_wtf import FlaskForm
from wtforms import validators as v


class AuthFormValues(t.TypedDict):
    password: str
    email: str


class AuthForm(FlaskForm):
    password = wtforms.PasswordField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    user = wtforms.EmailField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> AuthFormValues:
        return {
            "password": self.password.data,
            "email": self.user.data,
        }


class InstitutionsFormValues(t.TypedDict):
    page: int
    per_page: int


class InstitutionsForm(FlaskForm):
    page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )
    per_page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )

    def values(self) -> InstitutionsFormValues:
        return {
            "page": self.page.data or 1,
            "per_page": self.per_page.data or 1,
        }
