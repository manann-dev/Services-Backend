# schema/models/question.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..base import Base

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    grant_id = Column(Integer, ForeignKey('grants.id'))
    text = Column(String)
    response_type = Column(Enum('text', 'number', 'choice', name='response_type', default='text'))

    grant = relationship("Grant", back_populates="questions")
    choices = relationship("Choice", back_populates="question")
