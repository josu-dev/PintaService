import typing as t

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField
from wtforms import validators as v

from src.services.institution import InstitutionParams


class InstitutionForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    information = TextAreaField(
        "Información",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )
    address = StringField(
        "Dirección",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    location = StringField(
        "Ubicación",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    web = StringField(
        "Sitio web",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    keywords = StringField(
        "Palabras clave",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    email = EmailField(
        "Correo electrónico",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    days_and_opening_hours = StringField(
        "Días y Horarios de Apertura",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )

    def values(self) -> InstitutionParams:
        return {  # type: ignore
            "name": self.name.data,
            "information": self.information.data,
            "address": self.address.data,
            "location": self.location.data,
            "web": self.web.data,
            "keywords": self.keywords.data,
            "email": self.email.data,
            "days_and_opening_hours": self.days_and_opening_hours.data,
        }


class EmailFormValues(t.TypedDict):
    email: str


class EmailForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    def values(self) -> EmailFormValues:
        return {
            "email": self.email.data,  # type: ignore
        }
