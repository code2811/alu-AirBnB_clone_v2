#!/usr/bin/python3
""" Amenity module for DBStorage """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Amenity(BaseModel, Base):
    """ Amenity class for DBStorage """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Many-to-Many relationship to Place (defined in place.py)
    place_amenities = relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities"
    )

