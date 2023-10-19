import typing as t

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SelectField, StringField
from wtforms import validators as v

from src.core.enums import DocumentTypes, GenderOptions
from src.services.user import UserParams, UserUpdateParams


class ProfileUpdateForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    lastname = StringField(
        "Apellido",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_type = SelectField(
        "Tipo de Documento",
        choices=[(choice.name, choice.value) for choice in DocumentTypes],
    )
    document_number = StringField(
        "Número de documento",
        validators=[v.DataRequired(), v.Length(min=8, max=8)],
    )
    gender = SelectField(
        "Género",
        choices=[(choice.name, choice.value) for choice in GenderOptions],
    )
    gender_other = StringField(
        "Otro género",
        validators=[v.Optional(), v.Length(min=0, max=32)],
    )
    address = StringField(
        "Dirección",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    phone = StringField(
        "Teléfono",
        validators=[v.DataRequired()],
    )

    def values(self) -> UserUpdateParams:
        """Return form values as a dictionary"""

        return {
            "firstname": self.firstname.data,  # type: ignore
            "lastname": self.lastname.data,  # type: ignore
            "document_type": t.cast(DocumentTypes, self.document_type.data),
            "document_number": self.document_number.data,  # type: ignore
            "gender": t.cast(GenderOptions, self.gender.data),
            "gender_other": self.gender_other.data or "",  # type: ignore
            "address": self.address.data,  # type: ignore
            "phone": self.phone.data,  # type: ignore
        }


class UserSearchForm(FlaskForm):
    email = StringField("Correo Electrónico")
    is_active = SelectField(
        "Estado", choices=[("", "Todos"), ("1", "Activo"), ("0", "No Activo")]
    )


class UserCreateForm(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    lastname = StringField(
        "Apellido",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    username = StringField(
        "Nombre de usuario",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired(),
            v.Length(min=0, max=32),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    document_type = SelectField(
        "Tipo de Documento",
        choices=[(choice.name, choice.value) for choice in DocumentTypes],
    )
    document_number = StringField(
        "Número de documento",
        validators=[v.DataRequired(), v.Length(min=8, max=8)],
    )
    address = StringField(
        "Dirección",
        validators=[v.DataRequired(), v.Length(min=0, max=256)],
    )
    phone = StringField(
        "Teléfono",
        validators=[v.DataRequired()],
    )
    gender = SelectField(
        "Género",
        choices=[(choice.name, choice.value) for choice in GenderOptions],
    )
    gender_other = StringField(
        "Otro género",
        validators=[v.Optional(), v.Length(min=0, max=32)],
    )

    def values(self) -> UserParams:
        """Return form values as a dictionary"""

        return {  # type: ignore
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "username": self.username.data,
            "email": self.email.data,
            "password": self.password.data,
            "document_type": self.document_type.data,
            "document_number": self.document_number.data,
            "address": self.address.data,
            "phone": self.phone.data,
            "gender": self.gender.data,
            "gender_other": self.gender_other.data or "",
        }
