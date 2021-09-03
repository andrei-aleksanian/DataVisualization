"""
Utils functions for tests.

To be reused in other tests.
"""

from sqlalchemy_utils.functions import drop_database as dropDatabase, database_exists
from app.database.database import engine, SessionLocal
from app.database.schemas import ExampleCreate
from app.database.crud import createExample
from app.database import models


mockExample = {
    "name": "example",
    "description": "string",
    "dimension": 3
}


def createMockExample():
  """Creating a mock example in the database"""
  database = SessionLocal()
  createExample(database, ExampleCreate(**mockExample))
  database.close()


def cleanupDB(start: bool):
  """
  Dropping the test database.

  Used frequently to encapsulate tests as needed.
  """
  if database_exists(engine.url):
    dropDatabase(engine.url)

  if start:
    models.Base.metadata.create_all(bind=engine)
