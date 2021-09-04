"""utils to be used only for COVA and ANGEL"""
import math
import os

import numpy as np
from scipy.io import loadmat
from sklearn import preprocessing

from app.types.exceptions import RuntimeAlgorithmError
from app.types.dataGenerated import DataGenerated, DataGeneratedNumpy
from app.utils.environment import Env
from .dataDynamic import childrenToList

from ..lib.evaluation import neighbor_prev_disturb


env = os.environ.get("ENVIRONMENT")


def getNeighbours(data: DataGeneratedNumpy):
  """
  Returns neighbours and packs data into a typed class
  """
  *_, prevWrongInHigh, prevWrongInLow, prevPartsave = neighbor_prev_disturb(
      data["originalData"], data["resultData"], data["labels"], 10)

  return DataGenerated(
      points=data["resultData"].tolist(),
      labels=data["labels"].ravel().tolist(),
      prevPartsave=prevPartsave,
      prevWrongInLow=childrenToList(prevWrongInLow),
      prevWrongInHigh=childrenToList(prevWrongInHigh),
      dimension2D=data["dimension"] == 2
  )


def checkDimension(data: DataGeneratedNumpy):
  """
  Check and format target dimension of the data.
  Add 0's column to data if it is 2D (required for frontend)
  """
  if data["dimension"] == 2:
    zeros = np.zeros((data["resultData"].shape[0], 1))
    data["resultData"] = np.hstack((data["resultData"], zeros))
  return data


def toDataGenerated(data: DataGeneratedNumpy) -> DataGenerated:
  """Convert data to api friendly format"""
  data = checkDimension(data)
  return getNeighbours(data)


def loadData(filename: str):
  """Load data for an eaxmple"""
  fullData = loadmat(f'./app/visualization/Data/{filename}')
  xParam = fullData.get('x')

  sampleSize = 150
  if env == Env.PRODUCTION.value:
    sampleSize = len(xParam)

  scaler = preprocessing.MinMaxScaler()
  scaler.fit(np.array(xParam)[:sampleSize, :])
  data: np.ndarray = scaler.transform(np.array(xParam)[:sampleSize, :])
  labels: np.ndarray = np.array(fullData.get('label'))[
      :sampleSize, :].transpose()

  return data, labels, scaler


def getNeighbourNumber(pointsLength: int, neighbourNumber: str) -> int:
  """Get neighbour number as int"""
  if pointsLength == 0:
    raise RuntimeAlgorithmError("Can't divide by zero")

  if "%" not in neighbourNumber:
    return int(neighbourNumber)
  if neighbourNumber == '10%':
    return math.floor(pointsLength / 10)
  if neighbourNumber == '30%':
    return math.floor(pointsLength / 100 * 30)
  if neighbourNumber == '50%':
    return math.floor(pointsLength / 2)

  raise RuntimeAlgorithmError(f"Wrong neighbour value - {neighbourNumber}")
