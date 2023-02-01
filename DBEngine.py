from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.FilmDefinitions import Base

import os

DB_NAME = "site.db"
FILE_PATH = os.path.dirname(os.path.realpath('__file__'))

connection_string = "sqlite:///"+os.path.join(FILE_PATH, DB_NAME)+"?check_same_thread=False"

engine = create_engine(connection_string, echo=False)

Session = sessionmaker()

Base.metadata.create_all(engine)