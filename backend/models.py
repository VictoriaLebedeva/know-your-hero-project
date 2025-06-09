import os
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

# load variables for database connection
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class User(Base):
    """Defines the structure of the 'users' table in the database."""

    __tablename__ = "users"

    # Define table attributes
    id = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default="collegue")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class Review(DeclarativeBase):
    pass  # TBD


# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """Initializes the database by creating all tables."""
    Base.metadata.create_all(engine)