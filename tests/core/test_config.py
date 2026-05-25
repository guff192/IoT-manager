import pytest
from pydantic import ValidationError
from pydantic_settings import SettingsConfigDict
from app.core.config import Settings


def test_settings_initialization():
    """Test that settings can be initialized with required fields."""
    settings = Settings(
        CELERY_BROKER_URL="redis://localhost:6379/0",
        CELERY_RESULT_BACKEND="redis://localhost:6379/0",
        REDIS_URL="redis://localhost:6379/0",
        POSTGRES_HOSTNAME="localhost",
        POSTGRES_USER="user",
        POSTGRES_PASSWORD="password",
        POSTGRES_DB="dbname",
    )
    assert settings.API_V1_STR == "/api/v1"
    assert settings.POSTGRES_PORT == 5432
    assert settings.POSTGRES_USER == "user"


def test_sql_alchemy_database_url():
    """Test the computed SQLALCHEMY_DATABASE_URL property."""
    settings = Settings(
        CELERY_BROKER_URL="redis://localhost:6379/0",
        CELERY_RESULT_BACKEND="redis://localhost:6379/0",
        REDIS_URL="redis://localhost:6379/0",
        POSTGRES_HOSTNAME="test-host",
        POSTGRES_USER="test-user",
        POSTGRES_PASSWORD="test-password",
        POSTGRES_DB="test-db",
        POSTGRES_PORT=5433,
    )
    # The computed field returns a PostgresDsn, we check its string representation
    expected_url = "postgresql+asyncpg://test-user:test-password@test-host:5433/test-db"
    assert str(settings.SQLALCHEMY_DATABASE_URL) == expected_url


def test_settings_validation_error():
    """Test that missing required fields raise a ValidationError."""
    class MockSettings(Settings):
        model_config = SettingsConfigDict(env_file=None, extra="ignore")

    with pytest.raises(ValidationError):
        # Missing REDIS_URL and other required fields
        MockSettings(
            CELERY_BROKER_URL="redis://localhost:6379/0",
            CELERY_RESULT_BACKEND="redis://localhost:6379/0",
            # REDIS_URL is missing
            POSTGRES_HOSTNAME="localhost",
            POSTGRES_USER="user",
        )


def test_settings_defaults():
    """Test that default settings are correctly assigned."""
    settings = Settings(
        CELERY_BROKER_URL="redis://localhost:6379/0",
        CELERY_RESULT_BACKEND="redis://localhost:6379/0",
        REDIS_URL="redis://localhost:6379/0",
        POSTGRES_HOSTNAME="localhost",
        POSTGRES_USER="user",
    )
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60 * 24 * 7
