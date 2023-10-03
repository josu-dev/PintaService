from typing import TypedDict

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators as v

from src.services.auth import FullLoginUser, FullPreRegisterUser


class FullRegisterUser(TypedDict):
    username: str
    password: str
    password_con: str


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
            "email": self.email.data,
            "password": self.password.data,
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
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> FullPreRegisterUser:
        return {
            "firstname": self.firstname.data,
            "lastname": self.lastname.data,
            "email": self.email.data,
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
            "username": self.username.data,
            "password": self.password.data,
            "password_con": self.password_con.data,
        }
