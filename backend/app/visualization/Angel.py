"""
My angel functions
"""
from .lib.FunctionFile import AdjacencyMatrix
from .lib.ANGEL import AnchorPointGeneration, AnchorEmbedding, ANGEL_embedding

from ..types.dataGenerated import ParamsANGEL, DataGenerated, DataGeneratedNumpy
from ..types.Custom import Dimension

from .utils.dataGenerated import getNeighbourNumber, loadData, toDataGenerated


def runANGEL(params: ParamsANGEL, dimension: Dimension) -> DataGenerated:
  """Used for running ANGEL on every possible parameter"""
  originalData, labels, scaler = loadData("cylinder_top.mat")

  [anchorPoint, anchorLabel, zParam] = AnchorPointGeneration(
      originalData, labels, sparsity=params.anchorDensity)

  anchorpoint, _, _ = AnchorEmbedding(
      anchorPoint,
      anchorLabel,
      flagMove=1 if params.isAnchorModification else 0,
      lamb=params.lambdaParam,
      dim=dimension
  )
  scaler.fit(anchorpoint)
  anchorpoint = scaler.transform(anchorpoint)

  wParam = AdjacencyMatrix(
      originalData,
      neighbor=getNeighbourNumber(
          len(originalData), params.neighbourNumber),
      weight=0,
      metric='euclidean'
  )
  resultData = ANGEL_embedding(originalData, anchorpoint, zParam, wParam, dim=dimension,
                               T=15, eps=params.epsilon)

  return toDataGenerated(
      DataGeneratedNumpy({
          "originalData": originalData,
          "resultData": resultData,
          "labels": labels,
          "dimension": dimension
      })
  )
