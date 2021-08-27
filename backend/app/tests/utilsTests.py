"""
Utils functions for tests.

To be reused in other tests.
"""

from sqlalchemy_utils.functions import drop_database as dropDatabase
from app.database.database import engine
from app.database import models


def cleanupDB(start: bool):
  """
  Dropping the test database.

  Used frequently to encapsulate tests as needed.
  """
  dropDatabase(engine.url)

  if start:
    models.Base.metadata.create_all(bind=engine)
