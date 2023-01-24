import json
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

StaffFilmAssociationTable = Table(
    "staff_film_association_table",
    Base.metadata,
    Column("id_film", ForeignKey("films.id"), primary_key=True),
    Column("id_staff", ForeignKey("staff.id"), primary_key=True),
)

class Staff(Base):
    __tablename__="staff"

    id=Column(Integer, primary_key=True)
    first_name=Column(String(30), nullable=False, unique=False)
    last_name=Column(String(30), nullable=False, unique=False)

    speciality=Column(String(30), nullable=False, unique=False)

    def __init__(self, first_name, last_name, speciality):
        self.first_name = first_name
        self.last_name = last_name
        self.speciality = speciality

    @validates("first_name", "last_name", "speciality")
    def validate_name(self, key, value):
        assert value.isalpha()
        return value

    films_credited = relationship("Film", secondary=StaffFilmAssociationTable, overlaps="staff", back_populates="staff_credited")

    def toDict(self):
        return {
            "id" : str(self.id),
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "speciality" : self.speciality
        }

class Film(Base):
    __tablename__="films"

    id=Column(Integer, primary_key=True)
    name=Column(String(30), nullable=False, unique=True)
    description=Column(String(640), nullable=False, unique=False)
    release_date=Column(Integer, nullable=False, unique=False)

    def __init__(self, name, description, release_date):
        self.name = name
        self.description = description
        self.release_date = release_date

    @validates("name")
    def validate_name(self, key, value):
        assert all(x.isalpha() or x.isspace() or x.isnumeric() for x in value)
        return value

    @validates("description")
    def validate_description(self, key, value):
        assert all(x.isalpha() or x.isspace() or x.isnumeric() for x in value)
        return value

    staff_credited = relationship("Staff", secondary=StaffFilmAssociationTable, overlaps="films", back_populates="films_credited")
    
    def toDict(self):
        return {
            "id" : str(self.id),
            "name" : self.name,
            "description" : self.description,
            "release_date" : self.release_date
        }