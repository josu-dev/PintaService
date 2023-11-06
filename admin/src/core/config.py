import io
import os
import typing as t

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import Engine, create_engine, exc, sql


class ConfigurationError(Exception):
    """Error raised when a configuration error occurs.

    Attributes:
        message: A human-readable message describing the error.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def env_or_error(env: str, default: t.Union[str, None] = None) -> str:
    value = os.getenv(env, default)
    if value is None:
        raise ConfigurationError(f"Environment variable '{env}' not set")
    return value


def set_env_default(var: str, default: str) -> None:
    if os.getenv(var) is None:
        os.environ[var] = default


def preprocess_string(string: str) -> str:
    return string.replace("'", "''")


def print_query(title: str, query: str) -> None:
    print(title + "\n" + "-" * 79)
    print(query)
    print("-" * 79)


class TextFile(t.NamedTuple):
    __tablename__ = "text_file"

    name: str
    content: str
    id: t.Optional[int] = None


def create_table_query() -> str:
    return f"""
CREATE TABLE IF NOT EXISTS {TextFile.__tablename__} (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    content TEXT NOT NULL
);
""".lstrip()


def update_query(file: TextFile) -> str:
    return f"""
INSERT INTO {TextFile.__tablename__} (name, content)
VALUES ('{file.name}', '{preprocess_string(file.content)}')
ON CONFLICT (name) DO UPDATE
SET content = EXCLUDED.content;
""".lstrip()


def get_local_env_file() -> t.Union[TextFile, int]:
    path = input("Enter the path of the .env file: [.env.prod] ").strip()
    name = input("Enter the name for the .env file: [.env] ").strip()
    if not path:
        path = ".env.prod"
    if not name:
        name = ".env"

    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"[error]: env file '{name}' not found at path '{path}'")
        return 1

    env_file = TextFile(name=name, content=content)
    return env_file


def env_update() -> int:
    """Generates the SQL query to update the .env file in the database."""
    env_file = get_local_env_file()
    if isinstance(env_file, int):
        return env_file

    query = create_table_query() + update_query(env_file)
    print()
    print_query("ENV UPDATE QUERY", query)

    return 0


def db_uri_from_env() -> str:
    # DB config, environment variables names CAN'T be changed
    DB_USER = env_or_error("DB_USER")
    DB_PASS = env_or_error("DB_PASS")
    DB_HOST = env_or_error("DB_HOST")
    DB_PORT = env_or_error("DB_PORT", "5432")
    DB_NAME = env_or_error("DB_NAME")

    return f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_db_env_file(
    engine: Engine, name: str = ".env"
) -> t.Union[TextFile, int]:
    try:
        with engine.connect() as conn:
            result = conn.execute(
                sql.text(f"SELECT * FROM text_file WHERE name = '{name}'")
            ).first()
    except exc.SQLAlchemyError as e:
        print(f"[error]: during loading env file '{name}' \n{e}", flush=True)
        return 1

    if not result:
        print(
            f"[error]: env file '{name}' not found in database",
            flush=True,
        )
        return 1
    return TextFile(name=result[1], content=result[2])


def load_db_dotenv(name: str = ".env") -> int:
    engine = create_engine(db_uri_from_env())

    try:
        env_file = get_db_env_file(engine, name)
        if isinstance(env_file, int):
            return env_file
    finally:
        engine.dispose()

    loaded = load_dotenv(stream=io.StringIO(env_file.content), override=True)
    if not loaded:
        print(
            f"[error]: during loading env file '{name}'",
            flush=True,
        )
        return 1

    print(
        f"[success]: env file '{name}' loaded from database",
        flush=True,
    )
    return 0


class Config:
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    SQLALCHEMY_DATABASE_URI: str

    # Flask config
    SECRET_KEY: str

    # WTForms config
    WTF_CSRF_ENABLED: bool
    WTF_CSRF_SECRET_KEY: str
    WTF_CSRF_CHECK_DEFAULT: bool

    # Flask-livetw config
    LIVETW_DEV: bool

    # Flask session config
    SESSION_TYPE: str

    # Email credentials
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_SSL: bool
    MAIL_USE_TLS: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    # Google config
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    @classmethod
    def load_env_config(cls) -> None:
        # DB environment variables names CAN'T be changed
        cls.DB_USER = env_or_error("DB_USER")
        cls.DB_PASS = env_or_error("DB_PASS")
        cls.DB_HOST = env_or_error("DB_HOST")
        cls.DB_PORT = env_or_error("DB_PORT", "5432")
        cls.DB_NAME = env_or_error("DB_NAME")

        cls.SQLALCHEMY_TRACK_MODIFICATIONS = True
        cls.SQLALCHEMY_DATABASE_URI = f"postgresql://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"  # noqa: E501

        cls.SECRET_KEY = env_or_error("SECRET_KEY")

        cls.WTF_CSRF_ENABLED = (
            env_or_error("WTF_CSRF_ENABLED", "true").lower() == "true"
        )
        cls.WTF_CSRF_SECRET_KEY = env_or_error("WTF_CSRF_SECRET_KEY")
        cls.WTF_CSRF_CHECK_DEFAULT = (
            env_or_error("WTF_CSRF_CHECK_DEFAULT", "true").lower() == "true"
        )

        cls.LIVETW_DEV = env_or_error("LIVETW_DEV", "false").lower() == "true"

        cls.SESSION_TYPE = env_or_error("SESSION_TYPE", "filesystem")

        cls.MAIL_SERVER = env_or_error("MAIL_SERVER")
        cls.MAIL_PORT = int(env_or_error("MAIL_PORT"))
        cls.MAIL_USE_SSL = (
            env_or_error("MAIL_USE_SSL", "true").lower() == "true"
        )
        cls.MAIL_USE_TLS = (
            env_or_error("MAIL_USE_TLS", "false").lower() == "true"
        )
        cls.MAIL_USERNAME = env_or_error("MAIL_USERNAME")
        cls.MAIL_PASSWORD = env_or_error("MAIL_PASSWORD")
        cls.MAIL_DEFAULT_SENDER = env_or_error("MAIL_DEFAULT_SENDER")

        cls.GOOGLE_CLIENT_ID = env_or_error("GOOGLE_CLIENT_ID")
        cls.GOOGLE_CLIENT_SECRET = env_or_error("GOOGLE_CLIENT_SECRET")


def init_app(app: Flask, env: str) -> None:
    """Initializes the application configuration.

    Loads the environment variables from the .env file if the application
    is running in development mode, otherwise loads the environment variables
    from the database.
    """
    if env == "development":
        load_dotenv()
    else:
        load_db_dotenv()

    Config.load_env_config()

    app.config.from_object(Config)


def main() -> int:
    return env_update()


if __name__ == "__main__":
    raise SystemExit(main())
