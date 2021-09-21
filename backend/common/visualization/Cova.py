"""COVA algorithm to api communication"""

import numpy as np
from sklearn import preprocessing

from .lib.FunctionFile import funInit, AdjacencyMatrix
from .lib.evaluation import neighbor_prev_disturb
from .lib.COVA import ProtoGeneration,\
    CohortConfidence, COVAembedding, PrototypeEmbedding

from ..types.dataGenerated import DataGenerated, ParamsCOVA, DataGeneratedNumpy
from ..types.dataDynamic import DataDynamic, DataFormatted, DataNumpy
from ..types.Custom import Dimension

from .utils.dataGenerated import getNeighbourNumber, toDataGenerated, loadData, runAlgorithm
from .utils.dataDynamic import formatDataIn, formatDataOut,\
    childrenToList, splitData

# pylint: disable=R0913, R0914


def getCovaResult(params: ParamsCOVA,
                  dimension: Dimension,
                  iterations: int,
                  originalData: np.ndarray,
                  labels: np.ndarray,
                  scaler: preprocessing.MinMaxScaler):
  """Functoin that runs COVA"""
  dcParam, protolabel, clabel = ProtoGeneration(
      originalData,
      labels,
      C=0 if params.isCohortNumberOriginal else 1,
  )
  initdata, initanchor, _ = funInit(labels, protolabel, dim=dimension)
  vParam = PrototypeEmbedding(dcParam, protolabel, dim=dimension,
                              Embedding='SOE', init=initanchor)
  scaler.fit(vParam)
  vParam = scaler.transform(vParam)
  adjacencyMatrix = AdjacencyMatrix(
      originalData,
      getNeighbourNumber(
          len(originalData),
          params.neighbourNumber
      )
  )
  relation = CohortConfidence(originalData, clabel, 0)
  resultData: np.ndarray = COVAembedding(
      originalData,
      relation,
      adjacencyMatrix,
      vParam,
      initdata,
      dimension,
      params.alpha,
      iterations,
  )

  return relation, adjacencyMatrix, vParam, resultData


def runCOVA(params: ParamsCOVA,
            dimension: Dimension,
            originalData: np.ndarray,
            labels: np.ndarray,
            scaler: preprocessing.MinMaxScaler) -> DataGenerated:
  """Used for running COVA on every possible parameter"""
  *_, resultData = runAlgorithm(
      getCovaResult,
      params,
      dimension,
      20,
      originalData,
      labels,
      scaler
  )

  return toDataGenerated(
      DataGeneratedNumpy({
          "originalData": originalData,
          "resultData": resultData,
          "labels": labels,
          "dimension": dimension
      })
  )


def initCOVA(params: ParamsCOVA,
             dimension: Dimension,
             filePath: str) -> DataFormatted:
  """
  Initialise COVA run.

  Returns: original data set in 2d/3d space without optimisation
  """
  originalData, labels, scaler = loadData(filePath)

  relation, adjacencyMatrix, vParam, resultData = runAlgorithm(
      getCovaResult,
      params,
      dimension,
      0,
      originalData,
      labels,
      scaler
  )

  # formatting the data to be api friendly
  initData = DataNumpy({
      "originalData": originalData,
      "paramRelation": relation,
      "paramAd": adjacencyMatrix,
      "paramV": vParam,
      "labels": labels,
      "points": resultData,
      "alpha": params.alpha
  })

  return formatDataOut(initData)


def dynamicCOVA(previousData: DataDynamic,
                iterationsPerRequest: int) -> DataDynamic:
  """
  Iterates through the COVA algorithm.

  Inputs: all the data needed for COVA to run at a given point in time.
  As in, the algorithm is ready to pick up from any given point in the cycle
  provided the previous data is preserved.

  Returns: new data after a given number of iterations
  """
  data = formatDataIn(previousData)
  dimension = 2 if previousData.dimension2D else 3

  resultData: np.ndarray = runAlgorithm(
      COVAembedding,
      data["originalData"],
      data["paramRelation"],
      data["paramAd"],
      data["paramV"],
      data["points"],
      dimension,
      data["alpha"],
      iterationsPerRequest
  )

  # only run on the last iteration
  if previousData.iteration + 1 == previousData.maxIteration:
    *_, prevWrongInHigh, prevWrongInLow, prevPartsave = runAlgorithm(
        neighbor_prev_disturb,
        data["originalData"],
        resultData,
        data["labels"],
        10
    )
    previousData.prevWrongInHigh = childrenToList(prevWrongInHigh)
    previousData.prevWrongInLow = childrenToList(prevWrongInLow)
    previousData.prevPartsave = prevPartsave

  # mirror the format logic here
  resultData, points, _ = splitData(resultData)
  previousData.points = points.tolist()
  previousData.resultData = resultData.tolist()

  return previousData
