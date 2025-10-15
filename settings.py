import os
from dotenv import load_dotenv

# Ensure .env is loaded for os.getenv in local/dev and non-poetry environments
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=False)


def _get_env(name: str, default: str) -> str:
    # Support both UPPER and lower case env variable names
    return os.getenv(name) or os.getenv(name.lower()) or default


def _build_postgres_credentials() -> dict:
    host = _get_env("POSTGRES_HOST", "localhost")
    port = int(_get_env("POSTGRES_PORT", "5432"))
    database = _get_env("POSTGRES_DB", "mangosteen")
    user = _get_env("POSTGRES_USER", "mangosteen")
    password = _get_env("POSTGRES_PASSWORD", "mangosteen")
    return {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": _build_postgres_credentials(),
        }
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
