"""
Test generate ANGEL data
"""
import pytest
from examples_api.app.database.database import SessionLocal
from examples_api.app.database.crud import getAllExampleDataANGEL
from examples_api.app.visualization.generateANGEL import generateANGEL
from common.visualization.utils.dataGenerated import loadData
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

  originalData, labels, scaler = loadData(
      "./common/visualization/Data/bicycle_sample.mat")
  generateANGEL(1, 3, originalData, labels, scaler)

  database = SessionLocal()
  dataANGEL = getAllExampleDataANGEL(database, 1)
  database.close()

  assert len(dataANGEL) != 0

# test throw an error when the file is unreadable (to be implemented later)
