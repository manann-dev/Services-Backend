# schema/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True, unique=True)
    first_name = Column(String(50), nullable=False, unique=False)
    last_name = Column(String(50), nullable=False, unique=False)
    email = Column(String(100), nullable=False, unique=True)
    #password_hash = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    businesses = relationship("Business", back_populates="user")
    applications = relationship("Application", back_populates="user")
    
    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)
    
    def json(self):
        return{
            'id' : self.id,
            'username' : self.username,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email,
            'created_at' : self.created_at
        }