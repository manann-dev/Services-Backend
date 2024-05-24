# schema/models/response.py
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from ..base import Base

class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    text = Column(Text, nullable=True)  # For text responses
    choice_id = Column(Integer, ForeignKey('choices.id'), nullable=True)  # For choice responses, if applicable

    application = relationship("Application", back_populates="responses")
    question = relationship("Question")
    choice = relationship("Choice", back_populates="responses")  # If you're supporting choices in responses

    def __repr__(self):
        return f"<Response(application_id={self.application_id}, question_id={self.question_id}, text={self.text}, choice_id={self.choice_id})>"
