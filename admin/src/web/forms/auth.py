from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField
from wtforms import validators as v
from src.services.auth import FullLoginUser


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
