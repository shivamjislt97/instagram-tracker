from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from .database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    instagram_url = Column(String, unique=True)
    username = Column(String)

class ProfileHistory(Base):
    __tablename__ = "profile_history"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    bio = Column(String)
    bio_hash = Column(String)
    image_path = Column(String)
    image_hash = Column(String)
    checked_at = Column(DateTime, default=datetime.utcnow)
