"""
Utils functions for tests.

To be reused in other tests.
"""
import os
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import drop_database as dropDatabase, database_exists
from app.database.database import engine, SessionLocal
from app.database.schemas import ExampleCreate
from app.database.crud import createExample
from app.database import models
from app.utils.static import staticFolderPath


mockExample = {
    "name": "example",
    "description": "string",
    "dimension": 3,
}

mockExampleWithImage = {
    **mockExample,
    "imagePath": "test.jpg"
}


def getImage():
  """
  Get test imahge as bytes
  """
  return open(os.getcwd() + '/app/tests/files/test.jpg', 'rb')


def getMat():
  """
  Get test imahge as bytes
  """
  return open(os.getcwd() + '/app/tests/files/test.mat', 'rb')


def postMockExample(client: TestClient):
  """
  POSTing an example and hence generating test data for ANGEL and COVA
  """
  response = client.post("/api/examples/", data=mockExample,
                         files={"image": ("test.jpg", getImage(), "image/jpeg")})

  return response


def createMockExample():
  """Creating a mock example in the database"""
  database = SessionLocal()
  createExample(database, ExampleCreate(**mockExampleWithImage))
  database.close()


def cleanupDB(start: bool):
  """
  Dropping the test database.

  Used frequently to encapsulate tests as needed.
  """
  if database_exists(engine.url):
    dropDatabase(engine.url)

  for path in Path(staticFolderPath + '.').glob("*test.jpg"):
    path.unlink()

  if start:
    models.Base.metadata.create_all(bind=engine)
