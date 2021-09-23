"""
Utils functions for tests.

To be reused in other tests.
"""
import os
import json
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import drop_database as dropDatabase, database_exists
from examples_api.app.database.database import engine, SessionLocal
from examples_api.app.database.schemas import ExampleCreate
from examples_api.app.database.crud import createExample
from examples_api.app.database import models
from common.static import staticFolderPath, generatedDataFolderPath


mockExample = {
    "name": "example",
    "description": "string",
    "dimension": 3,
}

mockExampleWithImage = {
    **mockExample,
    "imagePath": "test.jpg",
    "filePath": "test.mat",
    "originalData": json.dumps([0]),
    "labels": json.dumps([0])
}


def getImage():
  """
  Get test imahge as bytes
  """
  return open(os.getcwd() + '/tests/files/test.jpg', 'rb')


def getMat():
  """
  Get test imahge as bytes
  """
  return open(os.getcwd() + '/tests/files/test.mat', 'rb')


def getBadMat():
  """
  Get bad test image as bytes
  """
  return open(os.getcwd() + '/tests/files/testBad.mat', 'rb')


def postMockExample(client: TestClient):
  """
  POSTing an example and hence generating test data for ANGEL and COVA
  """
  response = client.post("/api/examples/", data=mockExample,
                         files={
                             "image": ("test.jpg", getImage(), "image/jpeg"),
                             "file": ("test.mat", getMat(), ".mat")
                         })

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

  for path in Path(generatedDataFolderPath + '.').glob("*test.mat"):
    path.unlink()

  if start:
    models.Base.metadata.create_all(bind=engine)
