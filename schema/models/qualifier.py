# schema/models/qualifier.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..base import Base

class Qualifier(Base):
    __tablename__ = 'qualifiers'

    id = Column(Integer, primary_key=True)
    grant_id = Column(Integer, ForeignKey('grants.id'))
    description = Column(Text)
    criteria_type = Column(String) 
    criteria_value = Column(String) 

    grant = relationship("Grant", back_populates="qualifiers")
