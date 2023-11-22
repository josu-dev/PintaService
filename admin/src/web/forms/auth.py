from typing import TypedDict

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators as v

from src.services.auth import PreRegisterUserParams


class LoginFormValues(TypedDict):
    email: str
    password: str


class UserLogin(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )

    def values(self) -> LoginFormValues:
        return {  # type: ignore
            "email": self.email.data,
            "password": self.password.data,
        }


class UserPreRegister(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=64),
            v.Regexp(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b"),
        ],
    )

    def values(self) -> PreRegisterUserParams:
        return {  # type: ignore
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "email": self.email.data,
        }


class UserRegisterFormValues(TypedDict):
    username: str
    password: str
    password_confirmation: str


class UserRegisterGoogleFormValues(TypedDict):
    firstname: str
    lastname: str
    username: str
    password: str
    password_confirmation: str


class UserRegisterGoogle(FlaskForm):
    firstname = StringField(
        "Nombre",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    lastname = StringField(
        "Apellido",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    username = StringField(
        "Nombre de usuario",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
            v.EqualTo(
                "password_confirmation", message="Las contraseñas no coinciden"
            ),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )

    def values(self) -> UserRegisterGoogleFormValues:
        return {  # type: ignore
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "username": self.username.data,
            "password": self.password.data,
            "password_confirmation": self.password_confirmation.data,
        }


class UserRegister(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
            v.EqualTo(
                "password_confirmation", message="Las contraseñas no coinciden"
            ),
        ],
    )
    password_confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            v.DataRequired("Este campo es requerido"),
            v.Length(min=0, max=32),
        ],
    )

    def values(self) -> UserRegisterFormValues:
        return {  # type: ignore
            "username": self.username.data,
            "password": self.password.data,
            "password_confirmation": self.password_confirmation.data,
        }
