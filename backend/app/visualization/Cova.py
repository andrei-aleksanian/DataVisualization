"""COVA algorithm to api communication"""

import numpy as np
from scipy.spatial.distance import pdist, squareform

from .lib.SOEmbedding import SOE
from .lib.FunctionFile import funInit, AdjacencyMatrix
from .lib.evaluation import neighbor_prev_disturb
from .lib.COVA import ProtoGeneration,\
    CohortConfidence, COVAembedding, SeparateCohort, PrototypeEmbedding

from ..types.Custom import Dimension
from ..types.dataGenerated import DataGenerated, ParamsCOVA, DataGeneratedNumpy
from ..types.dataDynamic import DataDynamic, DataFormatted, DataNumpy

from .utils.dataGenerated import getNeighbourNumber, loadData, toDataGenerated
from .utils.dataDynamic import formatDataIn, formatDataOut, childrenToList


def runCOVA(params: ParamsCOVA, dimension: Dimension) -> DataGenerated:
  """Used for running COVA on every possible parameter"""
  originalData, labels, scaler = loadData("bicycle_sample.mat")

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
  relation = CohortConfidence(originalData, clabel, params.lambdaParam)
  resultData: np.ndarray = COVAembedding(
      originalData,
      relation,
      adjacencyMatrix,
      vParam,
      initdata,
      dimension,
      params.alpha,
      20,
  )

  return toDataGenerated(
      DataGeneratedNumpy({
          "originalData": originalData,
          "resultData": resultData,
          "labels": labels,
          "dimension": dimension
      })
  )


def initCOVA() -> DataFormatted:
  """
  Initialise COVA run.

  Returns: original data set in 2d/3d space without optimisation
  """
  originalData, labels, scaler = loadData("bicycle_sample.mat")

  prototypes, protolabel, clabel = SeparateCohort(
      originalData, labels, sparsity=0.1)
  aParam = squareform(pdist(prototypes, 'euclidean'))
  aOrder = np.argsort(aParam, axis=1).astype(int)
  vParam = SOE(aOrder.astype(int), protolabel, dim=3)
  scaler.fit(vParam)
  vParam = scaler.transform(vParam)

  adjacencyMatrix = AdjacencyMatrix(originalData, 10)

  print(clabel)
  relation = CohortConfidence(originalData, clabel, 0)

  resultData = COVAembedding(originalData, relation,
                             adjacencyMatrix, vParam, 0, dim=3, T=0)

  # formatting the data to be api friendly
  initData = DataNumpy({
      "g": originalData,
      "Relation": relation,
      "Ad": adjacencyMatrix,
      "V": vParam,
      "labels": labels,
      "points": resultData,
      "alpha": 0.5
  })

  return formatDataOut(initData)


def dynamicCOVA(previousData: DataDynamic, iterationsPerRequest: int) -> DataDynamic:
  """
  Iterates through the COVA algorithm.

  Inputs: all the data needed for COVA to run at a given point in time.
  As in, the algorithm is ready to pick up from any given point in the cycle
  provided the previous data is preserved.

  Returns: new data after a given number of iterations
  """
  data = formatDataIn(previousData)

  resultData = COVAembedding(
      data["g"],
      data["Relation"],
      data["Ad"],
      data["V"],
      data["points"],
      3,
      data["alpha"],
      iterationsPerRequest
  )

  previousData.points = resultData.tolist()

  # only run after the last iteration
  if previousData.iteration + 1 == previousData.maxIteration:
    *_, prevWrongInHigh, prevWrongInLow, prevPartsave = neighbor_prev_disturb(
        data["g"], resultData, data["labels"], 10)
    previousData.prevWrongInHigh = childrenToList(prevWrongInHigh)
    previousData.prevWrongInLow = childrenToList(prevWrongInLow)
    previousData.prevPartsave = prevPartsave

  return previousData
