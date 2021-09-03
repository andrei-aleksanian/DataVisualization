"""
Test generate ANGEL data
"""
import pytest
from app.database.database import SessionLocal
from app.database.crud import getAllExampleDataANGEL
from app.visualization.utils.generateANGEL import generateANGEL
from ...utilsTests import cleanupDB, createMockExample


@pytest.fixture(scope='function', autouse=True)
def afterAll():
  """
  Drop DB after all tests in class
  """
  cleanupDB(start=True)
  yield
  cleanupDB(start=False)


def testGenerateDataSuccess():
  """Successful data generation"""
  createMockExample()

  generateANGEL(1, 3)

  database = SessionLocal()
  dataANGEL = getAllExampleDataANGEL(database, 1)
  database.close()

  assert len(dataANGEL) != 0

# test throw an error when the file is unreadable (to be implemented later)
