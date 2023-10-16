from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import validators as v

from src.services.institution import PartialInstitutionConfig


class InstitutionForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    information = TextAreaField(
        "Información",
        validators=[v.DataRequired(), v.Length(min=0, max=512)],
    )
    address = StringField(
        "Dirección",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    location = StringField(
        "Ubicación",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    web = StringField(
        "Sitio web",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    keywords = StringField(
        "Palabras clave",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    email = StringField(
        "Correo electrónico",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    days_and_opening_hours = StringField(
        "Días y Horarios de Apertura",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )

    def values(self) -> PartialInstitutionConfig:  # Service Algo
        data = self.data
        data.pop("csrf_token")
        return PartialInstitutionConfig(**data)
