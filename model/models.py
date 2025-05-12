from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
