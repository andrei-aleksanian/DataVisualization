"""
Tests for dynamic.py
"""
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

initData = client.get("/api/dynamic/cova").json()


def testCovaDemoDynamicInitSuccess():
  """
  Test the function initialises a cycle for future iterations.
  """
  response = client.get("/api/dynamic/cova")
  assert response.status_code == 200

  data = response.json()
  assert data["points"] is not None
  assert len(data["points"][0]) == 3
  assert data["iteration"] == 0


def testCovaDemoDynamicSuccess():
  """
  Test the function can use data from get to perform a cycle.
  """
  response = client.post("/api/dynamic/cova", json=initData)
  responseData = response.json()
  assert response.status_code == 200
  assert initData["iteration"] + 1 == responseData["iteration"]
  # The rest of the fields will come after the schema is defined fully


def testCovaDemoDynamic422Partial():
  """
  Test partially incorrect data throws an error
  """
  incorrectData = {
      **initData,
      "points": True
  }
  response = client.post("/api/dynamic/cova", json=incorrectData)
  assert response.status_code == 422


def testCovaDemoDynamic422Full():
  """
  Test empty data throws an error
  """
  response = client.post("/api/dynamic/cova", json={})
  assert response.status_code == 422


def testCovaDemoDynamicPreservance():
  """Test returns perseverance data on last iteration"""
  initData["iteration"] = initData["maxIteration"] - 1
  response = client.post("/api/dynamic/cova", json=initData)

  assert response.json()["prevPartsave"] is not None
  assert response.json()["prevWrongInLow"] is not None
  assert response.json()["prevWrongInHigh"] is not None
