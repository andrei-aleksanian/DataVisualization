"""
Test generate COVA data
"""
import pytest
from examples_api.app.database.database import SessionLocal
from examples_api.app.database.crud import getAllExampleDataCOVA
from examples_api.app.visualization.generateCOVA import generateCOVA
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
  generateCOVA(1, 3, originalData, labels, scaler)

  database = SessionLocal()
  dataCOVA = getAllExampleDataCOVA(database, 1)
  database.close()

  assert len(dataCOVA) != 0

# test throw an error when the file is unreadable (to be implemented later)
