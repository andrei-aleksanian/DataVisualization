"""
Tests for examples.py
"""
# pylint: disable=C0116, C0115

import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.routers.examples import EXAMPLE_ALREADY_EXISTS
from app.database.crud import getAllExampleDataCOVA
from app.database.database import SessionLocal
from ..utilsTests import cleanupDB

client = TestClient(app)

dummyData = {
    "name": "example",
    "description": "string"
}


@pytest.fixture(scope="module", autouse=True)
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
  response = client.post("/api/examples/", json=dummyData)

  assert response.status_code == 200


def testCreateExampleNameExists400():
  """
  Test 400 name already exists

  Note: this test expects the testCreateExampleSuccess
  to be run before it. Such that an example with name 'example'
  has already been created.
  """
  response = client.post("/api/examples/", json=dummyData)

  assert response.status_code == 400
  assert response.json() == {"detail": EXAMPLE_ALREADY_EXISTS}


def testCreateExampleRequired422():
  """
  Test 422 name is required
  """
  response = client.post("/api/examples/", json={})

  assert response.status_code == 422


def testCreateExampleGenerateCOVAANGEL():
  """
  Generates COVA and ANGEL entries

  Note: ANGEL generation is not implemented yet
  """
  cleanupDB(start=True)
  client.post("/api/examples/", json=dummyData)

  database = SessionLocal()
  exampleCOVAData = getAllExampleDataCOVA(database, 1)
  database.close()
  assert len(exampleCOVAData) != 0

# should clean the DB if there is an exception in the algorithm and return 500
# this can only happen if we are serving our own dataset
# that functionality is not implemented yet
