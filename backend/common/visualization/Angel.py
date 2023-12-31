"""
My angel functions
"""
import numpy as np
from sklearn import preprocessing
from .lib.FunctionFile import AdjacencyMatrix, funInit
from .lib.evaluation import neighbor_prev_disturb
from .lib.ANGEL import AnchorPointGeneration, AnchorEmbedding, ANGEL_embedding

from ..types.dataGenerated import ParamsANGEL, DataGenerated, DataGeneratedNumpy
from ..types.dataDynamic import DataNumpyANGEL, DataFormattedANGEL, DataDynamicANGEL
from ..types.Custom import Dimension

from .utils.dataGenerated import getNeighbourNumber, toDataGenerated, loadData, runAlgorithm
from .utils.dataDynamic import formatDataOutANGEL, childrenToList, \
    splitData, formatDataInANGEL

# pylint: disable=R0913, R0914


def getAngelResult(params: ParamsANGEL,
                   dimension: Dimension,
                   iterations: int,
                   originalData: np.ndarray,
                   labels: np.ndarray,
                   scaler: preprocessing.MinMaxScaler,
                   fast: bool = False,
                   init: bool = False
                   ) -> DataGenerated:
  """Used for running ANGEL on every possible parameter"""
  [anchorPoint, anchorLabel, zParam] = AnchorPointGeneration(
      originalData, labels, sparsity=params.anchorDensity)
  initdata, initanchor, cinit = funInit(labels, anchorLabel, dimension)

  anchorPoint, _, _ = AnchorEmbedding(
      anchorPoint,
      anchorLabel,
      flagMove=1 if params.isAnchorModification else 0,
      lamb=0,
      dim=dimension,
      init=initanchor,
      cinit=cinit,
  )
  scaler.fit(anchorPoint)
  anchorPoint = scaler.transform(anchorPoint)

  neighbourParam = getNeighbourNumber(
      len(originalData), params.neighbourNumber)
  wParam = AdjacencyMatrix(
      originalData,
      neighbor=neighbourParam,
      weight=0,
      metric='euclidean'
  )

  if init:  # return initdata for nicer initial display
    return neighbourParam, anchorPoint, zParam, wParam, initdata

  resultData = ANGEL_embedding(
      originalData,
      anchorPoint,
      zParam,
      wParam,
      dim=dimension,
      init=initdata,
      T=iterations,
      eps=params.epsilon,
      optType="fast" if fast else "constrained",
      neighbor=neighbourParam
  )

  return neighbourParam, anchorPoint, zParam, wParam, resultData


def runANGEL(params: ParamsANGEL,
             dimension: Dimension,
             originalData: np.ndarray,
             labels: np.ndarray,
             scaler: preprocessing.MinMaxScaler) -> DataGenerated:
  """Used for running ANGEL on every possible parameter"""

  *_, resultData = runAlgorithm(
      getAngelResult,
      params,
      dimension,
      15,
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


def initANGEL(params: ParamsANGEL,
              dimension: Dimension,
              filePath: str) -> DataFormattedANGEL:
  """Used for running ANGEL on every possible parameter"""
  originalData, labels, scaler = loadData(filePath)

  neighbourParam, anchorPoint, zParam, wParam, resultData = runAlgorithm(
      getAngelResult,
      params,
      dimension,
      0,
      originalData,
      labels,
      scaler,
      True,  # fast
      True  # return initialisation only
  )

  initData = DataNumpyANGEL(**{
      "neighbourParam": neighbourParam,
      "anchorPoint": anchorPoint,
      "zParam": zParam,
      "wParam": wParam,
      "paramEps": params.epsilon,
      "originalData": originalData,
      "points": resultData,
      "labels": labels,
  })

  return formatDataOutANGEL(initData)


def dynamicANGEL(previousData: DataDynamicANGEL,
                 iterations: int) -> DataDynamicANGEL:
  """
  Iterates through the COVA algorithm.

  Inputs: all the data needed for COVA to run at a given point in time.
  As in, the algorithm is ready to pick up from any given point in the cycle
  provided the previous data is preserved.

  Returns: new data after a given number of iterations
  """
  data = formatDataInANGEL(previousData)
  dimension = 2 if previousData.dimension2D else 3

  resultData: np.ndarray = runAlgorithm(
      ANGEL_embedding,
      data["originalData"],
      data["anchorPoint"],
      data["zParam"],
      data["wParam"],
      "fast",
      dimension,
      data["points"],
      data["paramEps"],
      'euclidean',
      iterations,
      data["neighbourParam"]
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
