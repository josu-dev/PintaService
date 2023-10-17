import typing as t

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators as v

from src.core.models.service import ServiceType
from src.services.service import ServiceParams


class ServiceForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    laboratory = StringField(
        "Laboratorio",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    description = TextAreaField(
        "Descripción",
        validators=[v.DataRequired(), v.Length(min=0, max=512)],
    )
    keywords = StringField(
        "Palabras clave",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    service_type = SelectField(
        "Tipo de Servicio",
        choices=[(choice.name, choice.value) for choice in ServiceType],
        validators=[v.DataRequired()],
    )

    def values(self) -> ServiceParams:
        return {  # type:ignore
            "name": self.name.data,
            "laboratory": self.laboratory.data,
            "description": self.description.data,
            "keywords": self.keywords.data,
            "service_type": t.cast(ServiceType, self.service_type.data),
        }
