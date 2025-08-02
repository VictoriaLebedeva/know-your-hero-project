import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-key-for-dev-only")

    # Database
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "knowyourhero_dev")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres_dev")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "secret_dev")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    ACCESS_TOKEN_EXPIRES_SECONDS = int(
        os.environ.get("ACCESS_TOKEN_EXPIRES_SECONDS", 60)
    )  # 1 hour
    REFRESH_TOKEN_EXPIRES_SECONDS = int(
        os.environ.get("REFRESH_TOKEN_EXPIRES_SECONDS", 300)
    )  # 30 days


class DevelopmentConfig(Config):
    DEBUG = True

    ACCESS_TOKEN_EXPIRES_SECONDS = 300  # 5 minutes
    REFRESH_TOKEN_EXPIRES_SECONDS = 86400  # 1 day


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
