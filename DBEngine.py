from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.orm import relationship, validates

from FilmDefinitions import Base

import os

DB_NAME = "site.db"
FILE_PATH = os.path.dirname(os.path.realpath('__file__'))

connection_string = "sqlite:///"+os.path.join(FILE_PATH, DB_NAME)

engine = create_engine(connection_string, echo=True)

Base.metadata.create_all(engine)