from typing import TypedDict

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators as v

from src.services.auth import PreRegisterUserParams


class RegisterFormValues(TypedDict):
    username: str
    password: str
    password_con: str


class LoginFormValues(TypedDict):
    email: str
    password: str


class UserLogin(FlaskForm):
    email = EmailField(
        "Email",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> LoginFormValues:
        return {
            "email": self.email.data,  # type: ignore
            "password": self.password.data,  # type: ignore
        }


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
        validators=[
            v.DataRequired(),
            v.Length(min=0, max=32),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    def values(self) -> PreRegisterUserParams:
        return {
            "firstname": self.firstname.data,  # type: ignore
            "lastname": self.lastname.data,  # type: ignore
            "email": self.email.data,  # type: ignore
        }


class UserRegister(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired(),
            v.Length(min=0, max=32),
            v.EqualTo(
                "password_confirmation", message="Las contraseñas no coinciden"
            ),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> RegisterFormValues:
        return {
            "username": self.username.data,  # type: ignore
            "password": self.password.data,  # type: ignore
            "password_confirmation": self.password_confirmation.data,  # type: ignore # noqa: E501
        }
