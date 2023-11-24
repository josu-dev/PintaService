import typing as t

from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    FloatField,
    StringField,
    TextAreaField,
    ValidationError,
)
from wtforms import validators as v

from src.services.institution import InstitutionParams


class DecimalPlaces:
    def __init__(self, places):  # type:ignore
        self.places = places

    def __call__(self, form, field):  # type:ignore
        value = str(field.data)  # type:ignore
        decimal_places = value[::-1].find(".")
        if decimal_places > self.places:
            raise ValidationError(
                f"El campo debe tener un máximo de {self.places} decimales"
            )


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
    latitude = FloatField(
        "Latitud",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.NumberRange(
                min=-55,
                max=-25.672960,
                message="La latitud debe estar en el rango de Argentina -55 a -22.",  # noqa
            ),
            DecimalPlaces(20),
        ],
    )

    longitude = FloatField(
        "Longitud",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.NumberRange(
                min=-70,
                max=-54,
                message="La longitud debe estar en el rango de argentina -70 a -54.",  # noqa
            ),
            DecimalPlaces(20),
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
        location = f"{self.latitude.data},{self.longitude.data}"
        return {  # type: ignore
            "name": self.name.data,
            "information": self.information.data,
            "address": self.address.data,
            "location": location,
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
