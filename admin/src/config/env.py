import io
import os
import typing as t

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, exc, sql


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
    path = input("Enter the path to the .env file: [.env.prod] ").strip()
    name = input("Enter the name of the .env file: [.env] ").strip()
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
    env_file = get_local_env_file()
    if isinstance(env_file, int):
        return env_file

    query = create_table_query() + "\n\n" + update_query(env_file)
    print_query("ENV UPDATE QUERY", query)

    return 0


def get_db_uri() -> str:
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    return f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_db_env_file(
    engine: Engine, name: str = ".env"
) -> t.Union[TextFile, int]:
    try:
        with engine.connect() as conn:
            result = conn.execute(
                sql.text(f"SELECT * FROM text_file WHERE name = '{name}'")
            ).first()

            if not result:
                print(
                    f"[error]: env file '{name}' not found in database",
                    flush=True,
                )
                return 1
            return TextFile(name=result[1], content=result[2])
    except exc.SQLAlchemyError as e:
        print(f"[error]: during loading env file '{name}' \n{e}", flush=True)
        return 1


def load_envstr(env: str) -> int:
    try:
        loaded = load_dotenv(stream=io.StringIO(env), override=True)
    except Exception as e:
        print(
            f"[error]: during loading env string \n{e}",
            flush=True,
        )
        return 1

    return 0 if loaded else 1


def load_dbdotenv(name: str = ".env") -> int:
    engine = create_engine(get_db_uri())

    try:
        env_file = get_db_env_file(engine, name)
        if isinstance(env_file, int):
            return env_file

        loaded = load_envstr(env_file.content)
        if loaded > 0:
            print(
                f"[error]: during loading env file '{name}'",
                flush=True,
            )
            return 1

        print(
            f"[success]: env file '{name}' loaded from database",
            flush=True,
        )
        return loaded
    finally:
        engine.dispose()


def main() -> int:
    return env_update()


if __name__ == "__main__":
    raise SystemExit(main())
