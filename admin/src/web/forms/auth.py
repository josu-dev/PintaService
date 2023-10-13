from typing import TypedDict

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators as v

from src.services.auth import PreRegisterUserParams


class FullRegisterUser(TypedDict):
    username: str
    password: str
    password_con: str


class FullLoginUser(TypedDict):
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

    def values(self) -> FullLoginUser:
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
        "Username",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            v.DataRequired(),
            v.Length(min=0, max=32),
            v.EqualTo("password_con", message="Las contraseñas no coinciden"),
        ],
    )
    password_con = PasswordField(
        "Contraseña_con",
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> FullRegisterUser:
        return {
            "username": self.username.data,  # type: ignore
            "password": self.password.data,  # type: ignore
            "password_con": self.password_con.data,  # type: ignore
        }
