import os
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
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
    name = Column(String(256), nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), nullable=False, default="collegue")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
class RefreshToken(Base):
    """Defines the structure of the 'refresh_token' table in the database."""
    
    __tablename__ = "refresh_token"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    token_hash = Column(String(256), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    
    # relationships
    user = relationship("User", foreign_keys=[user_id])   

class Review(Base):
    """Defines the structure of the 'reviews' table in the database."""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    positive = Column(String(1000))
    negative = Column(String(1000))
    adresed_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User being reviewed
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # User who wrote the review
    created_at = Column(DateTime, default=datetime.now(timezone.utc))   
    
    # relationships
    adresed = relationship("User", foreign_keys=[adresed_id])  # Connects to reviewed user
    author = relationship("User", foreign_keys=[author_id])    # Connects to review author

# Database setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """Initializes the database by creating all tables."""
    Base.metadata.create_all(engine)