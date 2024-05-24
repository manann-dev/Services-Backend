# schema/models/choice.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base

class Choice(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    text = Column(String)

    question = relationship("Question", back_populates="choices")
    responses = relationship("Response", back_populates="choice")