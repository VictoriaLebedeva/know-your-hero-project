import os
from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship, mapped_column
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, text
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
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
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email = Column(String(120), nullable=False, unique=True)
    name = Column(String(256), nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default="collegue")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    failed_login_attempts = Column(Integer, nullable=False, default=0)
    lock_login_until = Column(DateTime(timezone=True), nullable=True)

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class RefreshToken(Base):
    """Defines the structure of the 'refresh_token' table in the database."""

    __tablename__ = "refresh_token"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash = Column(String(512), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)

    def set_token(self, token):
        """Hashes and sets the refresh_token."""
        self.token_hash = generate_password_hash(token)

    def check_token(self, token):
        """Checks if the provided refresh_token matches the stored hash."""
        return check_password_hash(self.token_hash, token)

    # relationships
    user = relationship("User", foreign_keys=[user_id])


class Review(Base):
    """Defines the structure of the 'reviews' table in the database."""

    __tablename__ = "reviews"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    positive = Column(String(1000))
    negative = Column(String(1000))
    recipient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # relationships
    recipient = relationship(
        "User", foreign_keys=[recipient_id]
    )  # Connects to reviewed user
    author = relationship("User", foreign_keys=[author_id])  # Connects to review author


# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """Initializes the database by creating all tables."""
    Base.metadata.create_all(engine)
