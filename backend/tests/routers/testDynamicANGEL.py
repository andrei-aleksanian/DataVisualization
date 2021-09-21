"""
Tests for dynamic.py
"""
# pylint: disable=redefined-outer-name
import pytest
from fastapi.testclient import TestClient
from custom_data_api.app.api import app
from ..utilsTests import getImage, getMat, getBadMat

mockData = {
    "neighbourNumber": 10,
    "anchorDensity": 0.1,
    "epsilon": 0.1,
    "isAnchorModification": False,
    "dimension": 2
}


@pytest.fixture
def client():
  """Get a test client that thas start and stop events"""
  with TestClient(app) as testClient:
    yield testClient


with TestClient(app) as mockClient:
  initData = mockClient.post("/api/dynamic/angel-init", mockData,
                             files={"file": ("test.mat", getMat())}).json()


def testAngelDemoDynamicInitSuccess(client: TestClient):
  """
  Test the function initialises a cycle for future iterations.
  """
  response = client.post("/api/dynamic/angel-init", mockData,
                         files={"file": ("test.mat", getMat())})

  assert response.status_code == 200

  data = response.json()
  assert data["points"] is not None
  assert len(data["points"][0]) == 3
  assert data["iteration"] == 0


def testAngelDemoDynamicInitFileFailiure(client: TestClient):
  """
  Test the function rejects a bad file. (no g vector and over 500 points limit)
  """
  response = client.post("/api/dynamic/angel-init", mockData,
                         files={"file": ("test.mat", getBadMat())})

  print(response.json())

  assert response.status_code == 422


def testAngelDemoDynamicInitImageFailiure(client: TestClient):
  """
  Test the function rejects a non .mat file.
  """
  response = client.post("/api/dynamic/angel-init", mockData,
                         files={"file": ("test.jpg", getImage())})

  print(response.json())

  assert response.status_code == 422


def testAngelDemoDynamicInitImageAsMatFailiure(client: TestClient):
  """
  Test the function rejects an image pretending to be a .mat file.
  """
  response = client.post("/api/dynamic/angel-init", mockData,
                         files={"file": ("test.mat", getImage())})

  print(response.json())

  assert response.status_code == 422


def testAngelDemoDynamicSuccess(client: TestClient):
  """
  Test the function can use data from get to perform a cycle.
  """
  response = client.post("/api/dynamic/angel", json=initData)
  responseData = response.json()
  assert response.status_code == 200
  assert initData["iteration"] + 1 == responseData["iteration"]


def testAngelDemoDynamic422Partial(client: TestClient):
  """
  Test partially incorrect data throws an error
  """
  incorrectData = {
      **initData,
      "points": True
  }
  response = client.post("/api/dynamic/angel", json=incorrectData)
  assert response.status_code == 422


def testAngelDemoDynamic422Full(client: TestClient):
  """
  Test empty data throws an error
  """
  response = client.post("/api/dynamic/angel", json={})
  assert response.status_code == 422


def testAngelDemoDynamicPreservance(client: TestClient):
  """Test returns perseverance data on last iteration"""
  initData["iteration"] = initData["maxIteration"] - 1
  response = client.post("/api/dynamic/angel", json=initData)

  data = response.json()
  assert data["prevPartsave"] is not None
  assert data["prevWrongInLow"] is not None
  assert data["prevWrongInHigh"] is not None
