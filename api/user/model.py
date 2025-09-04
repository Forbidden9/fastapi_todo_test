from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Relations
    tasks = relationship("Task", back_populates="owner")
