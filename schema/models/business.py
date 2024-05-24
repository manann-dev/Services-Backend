# schema/models/business.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import Base

class Business(Base):
    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    description = Column(Text)
    contact_email = Column(String)
    pitch_deck_url = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    industry = Column(String) 
    size = Column(Integer)  
    
    user = relationship("User", back_populates="businesses")
