import typing as t

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators as v

from src.core.enums import RequestStatus
from src.services.request import RequestParams


class RequestForm(FlaskForm):
    title = StringField(
        "Titulo",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    description = TextAreaField(
        "Descripcion",
        validators=[v.DataRequired(), v.Length(min=0, max=512)],
    )
    status = SelectField(
        "Estado",
        choices=[(choice.name, choice.value) for choice in RequestStatus],
        validators=[v.DataRequired()],
    )

    def values(self) -> RequestParams:
        return {  # type: ignore
            "title": self.title.data,
            "description": self.description.data,
            "status": t.cast(RequestStatus, self.status.data),
        }
