# config.py
import os
from config_example import DB_CONFIG as EXAMPLE

def _get_env(name, fallback=None):
    v = os.getenv(name)
    return v if v is not None else fallback

DB_CONFIG = {
    "host": _get_env("DB_HOST", EXAMPLE.get("host")),
    "user": _get_env("DB_USER", EXAMPLE.get("user")),
    "password": _get_env("DB_PASSWORD", EXAMPLE.get("password")),
    "database": _get_env("DB_NAME", EXAMPLE.get("database")),
    "port": int(_get_env("DB_PORT", EXAMPLE.get("port", 3306))),
}
