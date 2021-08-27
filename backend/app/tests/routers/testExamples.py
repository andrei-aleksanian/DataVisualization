"""
Tests for examples.py
"""
# pylint: disable=C0116, C0115

import pytest
from fastapi.testclient import TestClient
from app.api import app
from ..utilsTests import cleanupDB

client = TestClient(app)


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
  dummyData = {
      "name": "example",
      "description": "string"
  }
  response = client.post("/api/examples/", json=dummyData)

  assert response.status_code == 200
