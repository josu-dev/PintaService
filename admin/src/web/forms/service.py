from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms import validators as v

from src.core.models.service import ServiceTypes
from src.services.service import ServiceParams


class ServiceForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    description = TextAreaField(
        "Descripción",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )
    keywords = StringField(
        "Palabras clave",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=256),
        ],
    )
    service_type = SelectField(
        "Tipo de Servicio",
        choices=[(choice.name, choice.value) for choice in ServiceTypes],
        validators=[v.DataRequired("Este campo es requerido")],
    )
    enabled = BooleanField("Habilitado")

    def values(self) -> ServiceParams:
        return {  # type:ignore
            "name": self.name.data,
            "description": self.description.data,
            "keywords": self.keywords.data,
            "service_type": self.service_type.data,
            "enabled": self.enabled.data,
        }
