"""
Tests for examples.py
"""

import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.routers.exampleDataCOVA import PARAMS_DO_NOT_EXIST
from app.types.dataGenerated import ParamsCOVA
from ..utilsTests import cleanupDB, postMockExample

client = TestClient(app)

OBSCURE_NUMBER = 200


@pytest.fixture(scope='function', autouse=True)
def afterAll():
  """
  Drop DB after all tests in class
  """
  cleanupDB(start=True)
  yield
  cleanupDB(start=False)


def testGetCOVAExampleSuccess():
  """
  Test successful get example after creation
  """
  postMockExample(client)
  params = ParamsCOVA(**{
      "neighbourNumber": "10",
      "lambdaParam": 0,
      "alpha": 0.4,
      "isCohortNumberOriginal": False
  })
  response = client.post("api/examples/cova/data/get/1",
                         json=params.dict())

  assert response.status_code == 200
  assert response.json() is not None


def testGetANGELExampleFailiure():
  """
  Test successful get example after creation
  """
  postMockExample(client)
  params = ParamsCOVA(**{
      "neighbourNumber": "10",
      "lambdaParam": OBSCURE_NUMBER,
      "alpha": OBSCURE_NUMBER,
      "isCohortNumberOriginal": True
  })
  response = client.post("api/examples/cova/data/get/1",
                         json=params.dict())

  assert response.status_code == 404
  assert response.json() == {"detail": PARAMS_DO_NOT_EXIST}
