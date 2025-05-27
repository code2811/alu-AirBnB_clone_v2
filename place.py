#!/usr/bin/python3
""" Place module for DBStorage """

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

# Association table for many-to-many Place <-> Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)

class Place(BaseModel, Base):
    """ Place class for DBStorage """
    __tablename__ = 'places'
    # (other column definitions here...)

    # Many-to-Many relationship to Amenity
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        viewonly=False,
        back_populates="place_amenities"
    )

    # For FileStorage (if applicable)
    @property
    def amenities(self):
        """Getter for amenities linked to this Place."""
        from models import storage
        from models.amenity import Amenity
        amenity_list = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Setter for amenities linked to this Place."""
        if type(obj) == Amenity and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)

