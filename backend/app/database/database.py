"""
DB Session Creation
"""

# pylint: disable-all
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.environment import Env

env = os.environ.get("ENVIRONMENT")

SQLALCHEMY_DATABASE_URL = None

if env in [Env.DEV.value, Env.PRODUCTION.value]:
  SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
elif env == Env.TEST.value:
  SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
else:
  sys.exit("Please provide an environment variable ENVIRONMENT. \
  Choices are: DEV, PRODUCTION, TEST. E.g. \
  run: export ENVIRONMENT=DEV in your console")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False}  # delete connect_args later
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# TODO need to switch SQLite to MySQL
