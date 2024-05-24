# schema/models/grant.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from ..base import Base

class Grant(Base):
    __tablename__ = 'grants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    application_deadline = Column(DateTime)

    questions = relationship("Question", back_populates="grant")
    qualifiers = relationship("Qualifier", back_populates="grant")
    applications = relationship("Application", back_populates="grant")
