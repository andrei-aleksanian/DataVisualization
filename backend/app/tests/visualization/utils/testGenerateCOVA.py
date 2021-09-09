"""
Test generate COVA data
"""
import pytest
from app.database.database import SessionLocal
from app.database.crud import getAllExampleDataCOVA
from app.visualization.utils.generateCOVA import generateCOVA
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

  generateCOVA(1, 3)

  database = SessionLocal()
  dataCOVA = getAllExampleDataCOVA(database, 1)
  database.close()

  assert len(dataCOVA) != 0

# test throw an error when the file is unreadable (to be implemented later)