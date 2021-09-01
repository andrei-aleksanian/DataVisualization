"""utils to be used only for COVA and ANGEL"""
import math
import os

import numpy as np
from scipy.io import loadmat
from sklearn import preprocessing

from .lib.evaluation import neighbor_prev_disturb

from ..types.exceptions import RuntimeCOVAError
from ..types.Custom import Dimension
from ..types.dataGenerated import DataGenerated
from ..utils.environment import Env
from ..utils.dataDynamic import childrenToList


env = os.environ.get("ENVIRONMENT")


def toDataGenerated(
        originalData,
        resultData,
        labels,
        dimension: Dimension) -> DataGenerated:
  """Convert data to api friendly format"""
  print(f"originalData - {type(originalData)}")
  print(f"resultData - {type(resultData)}")
  print(f"labels - {type(labels)}")

  if dimension == 2:
    zeros = np.zeros((resultData.shape[0], 1))
    resultData = np.hstack((resultData, zeros))

  *_, prevWrongInHigh, prevWrongInLow, prevPartsave = neighbor_prev_disturb(
      originalData, resultData, labels, 10)

  return DataGenerated(
      points=resultData.tolist(),
      prevPartsave=prevPartsave,
      prevWrongInLow=childrenToList(prevWrongInLow),
      prevWrongInHigh=childrenToList(prevWrongInHigh),
      labels=labels.ravel().tolist(),
      dimension2D=dimension == 2
  )


def loadData(filename: str):
  """Load data for an eaxmple"""
  fullData = loadmat(f'./app/visualization/Data/{filename}')
  xParam = fullData.get('x')

  sampleSize = 150
  if env == Env.PRODUCTION.value:
    sampleSize = len(xParam)

  scaler = preprocessing.MinMaxScaler()
  scaler.fit(np.array(xParam)[:sampleSize, :])
  data = scaler.transform(np.array(xParam)[:sampleSize, :])
  labels = np.array(fullData.get('label'))[:sampleSize, :].transpose()

  return data, labels, scaler


def getNeighbourNumber(pointsLength: int, neighbourNumber: str) -> int:
  """Get neighbour number as int"""
  if "%" not in neighbourNumber:
    return int(neighbourNumber)
  if neighbourNumber == '10%':
    return math.floor(pointsLength / 10)
  if neighbourNumber == '30%':
    return math.floor(pointsLength / 100 * 30)
  if neighbourNumber == '50%':
    return math.floor(pointsLength / 2)

  raise RuntimeCOVAError("wrong neighbour value")

# test this
# figure out how to test visualisation code
