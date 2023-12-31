"""
Tests for utils module

formatDataIn is ignored as typing makes it unnecessary to check type conversions
"""
from typing import List
import numpy as np
from scipy.sparse.csr import csr_matrix
from common.visualization.utils.dataDynamic import childrenToList, toList, formatDataOut
from common.visualization.utils.dataGenerated import checkDimension, getNeighbourNumber, loadData
from common.types.dataDynamic import DataNumpy
from common.types.dataGenerated import DataGeneratedNumpy
from common.types.exceptions import RuntimeAlgorithmError


def getInputData(points):
  """
  Auxilary function that produces dummy data
  """
  npArray = np.array([0])
  csrArray = csr_matrix(npArray)
  labels = np.array([[0, 1, 2]])

  return DataNumpy(**{
      "points": points,
      "originalData": points,
      "labels": labels,
      "paramRelation": npArray,
      "paramAd": csrArray,
      "paramV": npArray,
      "alpha": 0
  })


def testFormatDataOut3D():
  """
  Check the function counts the 3D dimensions correctly,
  """

  points = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
  inputData = getInputData(points)

  data = formatDataOut(inputData)

  assert data.dimension2D is False


def testFormatDataOut2D():
  """
  Check the function counts the 2D dimensions correctly,
  adds 0 column
  """

  points = np.array([[0, 0], [0, 0], [0, 0]])
  inputData = getInputData(points)

  data = formatDataOut(inputData)

  assert data.dimension2D is True
  assert len(data.points[0]) == 3
  assert data.points[0][2] == 0


def testToList():
  """
  Test toList converts both np.ndarray and int to list
  """
  numpyInputArr = np.array([0])
  numpyInputInt = np.int64(0)

  myList = toList(numpyInputArr)

  assert isinstance(myList, list)
  assert myList[0] == numpyInputArr[0]
  assert myList[0] == numpyInputInt


def testChildrenToList():
  """
  Test childrenToList converts all np.ndarrays to lists
  """
  testDataNumpy = [np.array([0]), np.array([0])]

  myList = childrenToList(testDataNumpy)

  assert isinstance(myList[0], List)
  assert isinstance(myList[1], List)


dataGeneratedMock2D = DataGeneratedNumpy({
    "originalData": np.array([[0, 0], [1, 1]]),
    "resultData": np.array([[0, 0], [1, 1]]),
    "labels": np.array([[0, 1]]),
    "dimension": 2
})

dataGeneratedMock3D = DataGeneratedNumpy({
    "originalData": np.array([[0, 0, 0], [1, 1, 1]]),
    "resultData": np.array([[0, 0, 0], [1, 1, 1]]),
    "labels": np.array([[0, 1]]),
    "dimension": 3
})


def testCheckDimension2D():
  """Test checkDimension appends 0's column to 2D data"""
  resultData = checkDimension(dataGeneratedMock2D["resultData"])

  for point in resultData:
    assert point[2] == 0


def testCheckDimension3D():
  """Test checkDimension doesn't append 0's column to 3D data"""
  resultData = checkDimension(dataGeneratedMock3D["resultData"])

  assert np.array_equal(resultData, dataGeneratedMock3D["resultData"])


def testGetNeighbourNumber():
  """Test getNeighbourNumber converts a stringified integer into an int"""
  neighbourNumber = getNeighbourNumber(100, "10")

  assert neighbourNumber == 10


def testGetNeighbourNumberPercentage():
  """
  Test getNeighbourNumber converts a stringified integer with % into an int
  """
  neighbourNumber = getNeighbourNumber(200, "10%")
  assert neighbourNumber == 20

  neighbourNumber = getNeighbourNumber(200, "30%")
  assert neighbourNumber == 60


def testGetNeighbourNumberError():
  """
  Test getNeighbourNumber throws an error on invalid string
  """
  try:
    getNeighbourNumber(200, "100%")
  except RuntimeAlgorithmError:
    assert True


def testGetNeighbourNumberZeroLength():
  """
  Test 0 length throws an error
  """
  try:
    getNeighbourNumber(200, "100%")
  except RuntimeAlgorithmError:
    assert True


def testLoadData():
  """Load example data successfully"""
  data, labels, _ = loadData("./common/visualization/Data/bicycle_sample.mat")
  assert data.shape[0] == 150
  assert labels.shape[1] == 150
