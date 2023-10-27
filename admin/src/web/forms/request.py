import typing as t

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators as v

from src.core.enums import RequestStatus
from src.services.request import (
    RequestHistoryParams,
    RequestNoteParams,
    RequestParams,
)


class RequestForm(FlaskForm):
    title = StringField(
        "Titulo",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    description = TextAreaField(
        "Descripcion",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )
    status = SelectField(
        "Estado",
        choices=[(choice.name, choice.value) for choice in RequestStatus],
        validators=[v.DataRequired("Este campo es requerido")],
    )

    def values(self) -> RequestParams:
        return {  # type: ignore
            "title": self.title.data,
            "description": self.description.data,
            "status": t.cast(RequestStatus, self.status.data),
        }


class RequestNoteForm(FlaskForm):
    note = TextAreaField(
        "Notas",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )

    def values(self) -> RequestNoteParams:
        return {"note": self.note.data}  # type:ignore


class RequestHistoryForm(FlaskForm):
    status = SelectField(
        "Estado",
        choices=[(choice.name, choice.value) for choice in RequestStatus],
        validators=[v.DataRequired("Este campo es requerido")],
    )
    observations = TextAreaField(
        "Observaciones",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=512),
        ],
    )

    def values(self) -> RequestHistoryParams:
        return {  # type: ignore
            "status": t.cast(RequestStatus, self.status.data),
            "observations": self.observations.data,  # type: ignore
        }
