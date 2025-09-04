from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from api.task.enum import StateTask
from core.database.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    state = Column(String, default=StateTask.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relations
    owner = relationship("User", back_populates="tasks")
