from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators as v

from src.services.user import UpdateUserConfig, UserConfig


class UserCreateForm(FlaskForm):
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
        validators=[v.DataRequired(), v.Length(min=0, max=64)],
    )
    username = StringField(
        "Nombre de usuario",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_type = StringField(
        "Tipo de documento",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_number = StringField(
        "Número de documento",
        validators=[v.DataRequired(), v.Length(min=8, max=8)],
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
    phone = StringField("Telefono", [v.Length(min=0, max=16)])

    def values(self) -> UserConfig:
        return {
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "password": self.password.data,
            "email": self.email.data,
            "username": self.username.data,
            "document_type": self.document_type.data,
            "document_number": self.document_number.data,
            "gender": self.gender.data,
            "address": self.address.data,
            "phone": self.phone.data,
            "gender_other": self.gender_other.data,
        }


class UserUpdateForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    lastname = StringField(
        "Apellido",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_type = StringField(
        "Tipo de documento",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_number = StringField(
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
    phone = StringField("Telefono", [v.Length(min=0, max=16)])

    def values(self) -> UpdateUserConfig:
        return {
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "document_type": self.document_type.data,
            "document_number": self.document_number.data,
            "gender": self.gender.data,
            "gender_other": self.gender_other.data,
            "address": self.address.data,
            "phone": self.phone.data,
        }
