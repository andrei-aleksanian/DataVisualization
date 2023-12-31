"""
Tests for examples.py
"""

import pytest
from fastapi.testclient import TestClient
from examples_api.app.api import app
from examples_api.app.routers.examples import EXAMPLE_ALREADY_EXISTS
from examples_api.app.database.crud import getAllExampleDataCOVA, getAllExampleDataANGEL
from examples_api.app.database.database import SessionLocal
from ..utilsTests import cleanupDB, mockExample, \
    mockExampleWithImage, createMockExample, postMockExample

client = TestClient(app)


@pytest.fixture(scope='function', autouse=True)
def afterAll():
  """
  Drop DB after all tests in class
  """
  cleanupDB(start=True)
  yield
  cleanupDB(start=False)


def testCreateExampleSuccess():
  """
  Test successful create example
  """
  response = postMockExample(client)

  assert response.status_code == 200


def testCreateExampleNameExists400():
  """
  Test 400 name already exists
  """
  createMockExample()
  response = postMockExample(client)

  assert response.status_code == 400
  assert response.json() == {"detail": EXAMPLE_ALREADY_EXISTS}


def testCreateExampleRequired422():
  """
  Test 422 name is required
  """
  response = client.post("/api/examples/", data={})

  assert response.status_code == 422


def testCreateExampleGenerateCOVAANGEL():
  """
  Generates COVA and ANGEL entries
  """
  postMockExample(client)

  database = SessionLocal()
  exampleCOVAData = getAllExampleDataCOVA(database, 1)
  exampleANGELData = getAllExampleDataANGEL(database, 1)
  database.close()
  assert len(exampleCOVAData) != 0
  assert len(exampleANGELData) != 0

# should clean the DB if there is an exception in the algorithm and return 500
# this can only happen if we are serving our own dataset
# that functionality is not implemented yet, but will be at some point
# in the future


def testGetAllExamplesSuccessEmpty():
  """Get an empty array from empty database"""
  response = client.get("/api/examples/")

  assert response.json() == []


def testGetAllExamplesSuccessNotEmpty():
  """Post an example and then fetch it with get"""
  createMockExample()
  response = client.get("/api/examples/")

  mockResponseNoDimension = {**mockExampleWithImage}
  del mockResponseNoDimension["dimension"]
  del mockResponseNoDimension["filePath"]
  del mockResponseNoDimension["originalData"]
  del mockResponseNoDimension["labels"]
  mockResponseNoDimension["id"] = 1

  assert response.json() == [mockResponseNoDimension]


def testGetExampleSuccessNotEmpty():
  """Post an example and then fetch it with get"""
  postMockExample(client)
  response = client.get("/api/examples/1")

  originalData = response.json()["originalData"]
  dimension2D = response.json()["dimension2D"]

  assert response.status_code == 200
  assert originalData is not None
  assert dimension2D is not None
  assert dimension2D is (mockExample["dimension"] == 2)


def testGetExampleSuccessEmpty():
  """Fetch a non existing example with get"""
  response = client.get("/api/examples/1")

  assert response.status_code == 404
