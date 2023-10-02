from flask_wtf import FlaskForm
from typing_extensions import cast
from wtforms import EmailField, IntegerField, PasswordField, StringField
from wtforms import validators as v

from src.services.user import PartialUserConfig
from src.services.auth import FullPreRegisterUser


class UserUpdateForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    lastname = StringField(
        "Apellido",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    email = EmailField(
        "Email",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    username = StringField(
        "Nombre de usuario",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_type = StringField(
        "Tipo de documento",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_number = IntegerField(
        "Número de documento",
        validators=[v.DataRequired(), v.Length(min=0, max=8)],
    )
    gender = StringField(
        "Género",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    gender_other = StringField(
        "Otro género",
        validators=[v.Optional(), v.Length(min=0, max=32)],
    )
    address = StringField(
        "Dirección",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    phone = IntegerField(
        "Teléfono",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> PartialUserConfig:
        data = self.data  # type: ignore
        data.pop("csrf_token")
        return cast(PartialUserConfig, data)


class UserPreRegister(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    lastname = StringField(
        "Apellido",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    email = EmailField(
        "Email",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> FullPreRegisterUser:
        return {
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "email": self.email.data,
        }
