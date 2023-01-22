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

    position=Column(String(30), nullable=False, unique=False)

    @validates("first_name", "last_name", "position")
    def validate_first_name(self, key, value):
        assert value.isalpha()
        return value

    films = relationship("Film", secondary=StaffFilmAssociationTable, backref="staff")

class Film(Base):
    __tablename__="films"

    id=Column(Integer, primary_key=True)
    name=Column(String(30), nullable=False, unique=True)
    description=Column(String(640), nullable=False, unique=False)
    release_date=Column(DateTime)

    @validates("first_name")
    def validate_first_name(self, key, value):
        assert value.isalpha()
        return value

    @validates("description")
    def validate_first_name(self, key, value):
        assert value.isalpha() and value.isalnum()
        return value

    staff = relationship("Staff", secondary=StaffFilmAssociationTable, backref="films")
