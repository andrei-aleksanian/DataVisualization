"""
Tests for api routes:

Examples route
Dynamic routes
"""
from fastapi.testclient import TestClient
from ..api import app

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

  # The rest of the fields will come after the schema is defined fully


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
  initData.pop("points")
  response = client.post("/api/dynamic/cova", json=initData)
  assert response.status_code == 422


def testCovaDemoDynamic422Full():
  """
  Test empty data throws an error
  """
  response = client.post("/api/dynamic/cova", json={})
  assert response.status_code == 422

# Test returns perseverance data on last iteration
