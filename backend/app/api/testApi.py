"""
Tests for api routes
"""
from fastapi.testclient import TestClient
from .api import app

client = TestClient(app)


def testReadMain():
  """
  Test Basic COVA Demo
  """
  response = client.get("/api/cova-demo")
  assert response.status_code == 200
