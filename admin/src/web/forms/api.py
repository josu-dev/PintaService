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
            "password": self.password.data,  # type: ignore
            "email": self.user.data,  # type: ignore
        }


class PaginationFormValues(t.TypedDict):
    page: int
    per_page: int


class PaginationForm(FlaskForm):
    page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )
    per_page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )

    def values(self) -> PaginationFormValues:
        return {
            "page": self.page.data or 1,
            "per_page": self.per_page.data or 1,
        }


class ServiceFormValues(t.TypedDict):
    title: str
    description: str


class ServiceForm(FlaskForm):
    title = wtforms.StringField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    description = wtforms.StringField(
        validators=[v.DataRequired(), v.Length(min=0, max=512)],
    )

    def values(self) -> ServiceFormValues:
        return {
            "title": self.title.data or 1,  # type: ignore
            "description": self.description.data or 1,  # type: ignore
        }


class TextFormValues(t.TypedDict):
    text: str


class TextForm(FlaskForm):
    text = wtforms.StringField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> ServiceFormValues:
        return {
            "text": self.text.data or 1,  # type: ignore
        }


class ServiceSearchFormValues(t.TypedDict):
    q: str
    type: str
    page: int
    per_page: int


class ServiceSearchForm(FlaskForm):
    q = wtforms.StringField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    type = wtforms.StringField(
        validators=[v.Optional(), v.Length(min=0, max=32)],
    )
    page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )
    per_page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )

    def values(self) -> ServiceSearchFormValues:
        return {
            "q": self.q.data,
            "type": self.type.data,
            "page": self.page.data or 1,
            "per_page": self.per_page.data or 1,  # type: ignore
        }
