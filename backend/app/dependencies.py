"""
Dependencies.

Helpers for the API. e.g. getting a DB connection instance with cleanup.
"""

from .database.database import SessionLocal


def getDB():
  """
  Generating a single use instance of the session.
  Which closes connection once it's not needed anymore.
  """
  database = SessionLocal()
  try:
    yield database
  finally:
    database.close()
