"""
Tests for utils module

formatDataIn is ignored as typing makes it unnecessary to check type conversions
"""
from typing import List
import numpy as np
from dataDynamic import childrenToList, toList, formatDataOut, ListPerseverance, NumpyInput
from app.types.dataDynamic import DataNumpy


def getInputData(points):
  """
  Auxilary function that produces dummy data
  """
  npArray = np.array([0])
  labels = np.array([[0]])

  return DataNumpy(**{
      "points": points,
      "g": npArray,
      "labels": labels,
      "Relation": npArray,
      "Ad": npArray,
      "V": npArray,
      "alpha": 0
  })


def testFormatDataOut3D():
  """
  Check the function counts the 3D dimensions correctly,
  """

  points = np.array([[0, 0, 0]])
  inputData = getInputData(points)

  data = formatDataOut(inputData)

  assert data.dimension2D is False


def testFormatDataOut2D():
  """
  Check the function counts the 2D dimensions correctly,
  adds 0 column
  """

  points = np.array([[0, 0]])
  inputData = getInputData(points)

  data = formatDataOut(inputData)

  assert data.dimension2D is True
  assert len(data.points[0]) == 3
  assert data.points[0][2] == 0


def testToList():
  """
  Test toList converts both np.ndarray and int to list
  """
  numpyInputArr: NumpyInput = np.array([0])
  numpyInputInt: NumpyInput = np.int64(0)

  myList = toList(numpyInputArr)

  assert isinstance(myList, list)
  assert myList[0] == numpyInputArr[0]
  assert myList[0] == numpyInputInt


def testChildrenToList():
  """
  Test childrenToList converts all np.ndarrays to lists
  """
  testDataNumpy: ListPerseverance = [np.array([0]), np.array([0])]

  myList = childrenToList(testDataNumpy)

  assert isinstance(myList[0], List)
  assert isinstance(myList[1], List)
