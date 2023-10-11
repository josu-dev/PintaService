from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms import validators as v

from src.core.models.service import ServiceType
from src.services.service import PartialServiceConfig


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
        choices=[
            (ServiceType.ANALYSIS.value, "Análisis"),
            (ServiceType.CONSULTANCY.value, "Consulta"),
            (ServiceType.DEVELOPMENT.value, "Desarrollo"),
        ],
        validators=[v.DataRequired()],
    )

    def values(self) -> PartialServiceConfig:
        data = self.data
        data["service_type"] = ServiceType(data["service_type"])
        data.pop("csrf_token")
        return PartialServiceConfig(**data)
