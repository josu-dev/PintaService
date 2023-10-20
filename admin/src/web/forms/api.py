import typing as t

import wtforms
from flask_wtf import FlaskForm
from wtforms import validators as v


class AuthFormValues(t.TypedDict):
    password: str
    email: str


class AuthForm(FlaskForm):
    password = wtforms.PasswordField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    user = wtforms.EmailField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
        ],
    )

    def values(self) -> AuthFormValues:
        return {  # type: ignore
            "password": self.password.data,
            "email": self.user.data,
        }


class PaginationFormValues(t.TypedDict):
    page: int
    per_page: t.Union[int, None]


class PaginationForm(FlaskForm):
    page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )
    per_page = wtforms.IntegerField(
        validators=[v.Optional(), v.NumberRange(min=1, max=100)],
    )

    def values(self) -> PaginationFormValues:
        return {"page": self.page.data or 1, "per_page": self.per_page.data}


class ServiceRequestFormValues(t.TypedDict):
    service_id: int
    title: str
    description: str


class ServiceRequestForm(FlaskForm):
    service_id = wtforms.IntegerField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.NumberRange(min=0),
        ],
    )
    title = wtforms.StringField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    description = wtforms.StringField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )

    def values(self) -> ServiceRequestFormValues:
        return {  # type: ignore
            "service_id": self.service_id.data,
            "title": self.title.data,
            "description": self.description.data,
        }


class RequestNoteFormValues(t.TypedDict):
    text: str


class RequestNoteForm(FlaskForm):
    text = wtforms.StringField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=8, max=512),
        ],
    )

    def values(self) -> RequestNoteFormValues:
        return {"text": self.text.data}  # type: ignore


class ServiceSearchFormValues(t.TypedDict):
    q: str
    type: str
    page: int
    per_page: t.Union[int, None]


class ServiceSearchForm(FlaskForm):
    q = wtforms.StringField(
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
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
        return {  # type: ignore
            "q": self.q.data,
            "type": self.type.data,
            "page": self.page.data or 1,
            "per_page": self.per_page.data,
        }
