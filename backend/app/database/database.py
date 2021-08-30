"""
DB Session Creation
"""

import os
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.environment import Env

env = os.environ.get("ENVIRONMENT")
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("HOST_MYSQL")
database = os.environ.get("MYSQL_DATABASE")

engine: Engine = None

if env in [Env.DEV.value, Env.PRODUCTION.value]:
  engine = create_engine(
      f"mysql+pymysql://{user}:{password}@{host}/{database}")

elif env == Env.TEST.value:
  engine = create_engine("sqlite:///./test.db", connect_args={
      "check_same_thread": False}  # delete connect_args later
  )
else:
  sys.exit("Please provide an environment variable ENVIRONMENT. \
  Choices are: DEV, PRODUCTION, TEST. E.g. \
  run: export ENVIRONMENT=DEV in your console")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def setUpDatabase():
  """
  Reconnect to the database on failiure.
  Try every 5 seconds.
  """
  isDbConnected = False
  while not isDbConnected:
    try:
      Base.metadata.create_all(bind=engine)
      isDbConnected = True
    # pylint: disable=W0703
    except BaseException:
      time.sleep(5)
