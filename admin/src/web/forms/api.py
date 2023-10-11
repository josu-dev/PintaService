import typing as t

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import validators as v

AnyJSONBody = t.Dict[
    str,
    t.Union[str, int, float, bool, None, t.List[t.Any], t.Dict[str, t.Any]],
]


class AuthFormValues(t.TypedDict):
    password: str
    email: str


class AuthForm(FlaskForm):
    password = PasswordField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )
    user = EmailField(
        validators=[v.DataRequired(), v.Length(min=0, max=32)],
    )

    def values(self) -> AuthFormValues:
        return {
            "password": self.password.data,
            "email": self.user.data,
        }
