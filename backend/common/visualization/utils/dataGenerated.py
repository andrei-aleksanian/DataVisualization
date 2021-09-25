"""utils to be used only for COVA and ANGEL"""
import math
import os

import numpy as np
from scipy.io import loadmat
from sklearn import preprocessing

from common.types.exceptions import RuntimeAlgorithmError, FileConstraintsError
from common.types.dataGenerated import DataGenerated, DataGeneratedNumpy
from common.environment import Env
from .dataDynamic import childrenToList

from ..lib.evaluation import neighbor_prev_disturb
from ..lib.FunctionFile import postProcessing


env = os.environ.get("ENVIRONMENT")


def runAlgorithm(algorithmCallback, *args):
  """wrap algorithm functions in try and catch"""
  try:
    returnArgs: tuple = algorithmCallback(*args)
    return returnArgs
  except Exception as error:
    raise RuntimeAlgorithmError(
        "failed to run. Please, make sure your file is correct") from error


def getNeighbours(data: DataGeneratedNumpy):
  """
  Returns neighbours and packs data into a typed class
  """
  *_, prevWrongInHigh, prevWrongInLow, prevPartsave = neighbor_prev_disturb(
      data["originalData"], data["resultData"], data["labels"], 10)
  resultData = postProcessing(data["resultData"], data["dimension"])
  resultData = checkDimension(resultData)

  return DataGenerated(
      points=resultData.tolist(),
      labels=data["labels"].ravel().tolist(),
      prevPartsave=prevPartsave,
      prevWrongInLow=childrenToList(prevWrongInLow),
      prevWrongInHigh=childrenToList(prevWrongInHigh),
      dimension2D=data["dimension"] == 2
  )


def checkDimension(resultData: np.ndarray):
  """
  Check and format target dimension of the data.
  Add 0's column to data if it is 2D (required for frontend)
  """
  if resultData.shape[1] == 2:
    zeros = np.zeros((resultData.shape[0], 1))
    resultData = np.hstack((resultData, zeros))
  return resultData


def toDataGenerated(data: DataGeneratedNumpy) -> DataGenerated:
  """Convert data to api friendly format"""
  return getNeighbours(data)


def validateData(data: np.ndarray, labels: np.ndarray):
  """Validate the file constraints"""
  if data is None:
    raise FileConstraintsError(
        "The file must contain a dataset with the name g")
  if labels is None:
    raise FileConstraintsError(
        "The file must contain labels with the name label")
  if data.shape[0] > 500:
    raise FileConstraintsError("The file must contain no more than 500 points")
  if data.shape[0] not in [labels.shape[0], labels.shape[1]]:
    raise FileConstraintsError(
        "You should have a label exactly for each point in your dataset")


def loadData(filePath: str):
  """Load data for an eaxmple"""
  try:
    fullData = loadmat(filePath)
  except Exception as error:
    raise FileConstraintsError(
        "This file can't be processed as a mat file. Please, choose a different one.") from error
  originalData: np.ndarray = fullData.get('g')
  labels: np.ndarray = fullData.get('label')
  scaler = preprocessing.MinMaxScaler()

  validateData(originalData, labels)

  sampleSize = len(originalData)
  if env in [Env.TEST.value]:
    sampleSize = 150

  scaler.fit(originalData[:sampleSize, :])
  originalData = scaler.transform(originalData[:sampleSize, :])
  labels = labels[:sampleSize, :].transpose()

  return originalData, labels, scaler


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

  raise RuntimeAlgorithmError(f"Wrong neighbour value - {neighbourNumber}")
