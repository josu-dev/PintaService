from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth = OAuth()


def init_app(app: Flask) -> None:
    oauth.init_app(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",  # noqa: E501
        client_kwargs={"scope": "openid email profile"},
    )
