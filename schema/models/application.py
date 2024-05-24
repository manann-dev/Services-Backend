# schema/models/application.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import Base

class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    grant_id = Column(Integer, ForeignKey('grants.id'))
    submission_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='Pending')

    user = relationship("User", back_populates="applications")
    grant = relationship("Grant", back_populates="applications")
    responses = relationship("Response", back_populates="application")
