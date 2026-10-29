from app.db import normalize_db_url


def test_normalize_neon_url():
    url = "postgresql://u:p@ep-x.neon.tech/db?sslmode=require"
    assert normalize_db_url(url) == "postgresql+psycopg://u:p@ep-x.neon.tech/db?sslmode=require"
    assert normalize_db_url("postgres://u@h/db").startswith("postgresql+psycopg://")
    assert normalize_db_url("sqlite:///./app.db") == "sqlite:///./app.db"
