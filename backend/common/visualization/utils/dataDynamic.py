"""
utils functions for dynamic data loading
"""
from typing import List, NewType
import numpy as np
from sklearn.decomposition import PCA
from common.types.dataDynamic import DataDynamic, DataNumpy, DataFormatted,\
    DataNumpyANGEL, DataFormattedANGEL, DataDynamicANGEL
from common.types.Custom import Dimension
from common.visualization.lib.FunctionFile import postProcessing


def preserveOrientation(points: np.ndarray, dimension) -> np.ndarray:
  """Rotates the dataset to set it to a ficed orientation. Used after embedding."""
  pca = PCA(n_components=dimension)
  pca.fit(points)
  return pca.transform(points)


def formatDataInANGEL(previousData: DataDynamicANGEL) -> DataNumpyANGEL:
  """
  Reformat ANGEL input data to np.arrays
  """
  if previousData.dimension2D:
    previousData.points = np.delete(previousData.points, 2, 1)

  return DataNumpyANGEL(**{
      "paramEps": previousData.paramEps,
      "anchorPoint": np.array(previousData.anchorPoint),
      "zParam": np.array(previousData.zParam),
      "wParam": np.array(previousData.wParam),
      "originalData": np.array(previousData.originalData),
      "labels": np.array([previousData.labels]),
      "points": np.array(previousData.resultData)
  })


def formatDataIn(previousData: DataDynamic) -> DataNumpy:
  """
  Reformat input data from lists to np.arrays
  """
  if previousData.dimension2D:
    previousData.points = np.delete(previousData.points, 2, 1)

  return DataNumpy(**{
      "alpha": previousData.alpha,
      "points": np.array(previousData.resultData),
      "originalData": np.array(previousData.originalData),
      "labels": np.array([previousData.labels]),
      "paramRelation": np.array(previousData.paramRelation),
      "paramAd": np.array(previousData.paramAd),
      "paramV": np.array(previousData.paramV),
  })


def getDimension(points: np.ndarray) -> Dimension:
  """Return dimension of a data set."""
  return 2 if points.shape[1] == 2 else 3


def formatDimension(points: np.ndarray, dimension: Dimension):
  """Format and return points array."""
  if dimension == 2:
    zeros = np.zeros((points.shape[0], 1))
    points = np.hstack((points, zeros))

  return points


def splitData(data: np.ndarray):
  """Split the data into post processed and reusable."""
  resultData: np.ndarray = np.copy(data)

  dimension = getDimension(data)
  print(dimension)
  data = postProcessing(data, dimension)
  data = formatDimension(data, dimension)

  return resultData, data, dimension


def formatDataOutANGEL(initData: DataNumpyANGEL) -> DataFormattedANGEL:
  """
  Reformat input data from np.arrays to lists.
  Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
  Only runs once when a request is intialised for ANGEL.
  """
  resultData, initData["points"], dimension = splitData(initData["points"])

  return DataFormattedANGEL(**{
      **initData,
      "anchorPoint": initData["anchorPoint"].tolist(),
      "zParam": initData["zParam"].tolist(),
      "wParam": initData["wParam"].tolist(),
      "originalData": initData["originalData"].tolist(),
      "resultData": resultData.tolist(),
      "labels": initData["labels"].ravel().tolist(),
      "points": initData["points"].tolist(),
      "dimension2D": dimension == 2,
  })


def formatDataOut(initData: DataNumpy) -> DataFormatted:
  """
  Reformat input data from np.arrays to lists.
  Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
  Only runs once when a request is intialised.
  """
  resultData, initData["points"], dimension = splitData(initData["points"])

  return DataFormatted(**{
      **initData,
      "originalData": initData["originalData"].tolist(),
      "resultData": resultData.tolist(),
      "points": initData["points"].tolist(),
      "labels": initData["labels"].ravel().tolist(),
      "dimension2D": dimension == 2,
      "paramRelation": initData["paramRelation"].tolist(),
      "paramAd": initData["paramAd"].tolist(),
      "paramV": initData["paramV"].tolist(),
  })


NumpyInput = NewType('NumpyInput', np.ndarray or np.int64)


def toList(numpyArray: NumpyInput) -> List:
  """
  Converting np.ndarray to list.
  If np.int64 is passed, [np.int64] is returned.
  """
  if isinstance(numpyArray, np.int64):
    return [numpyArray]

  return numpyArray.tolist()


ListPerseverance = NewType('ListPerseverance', List[NumpyInput])


def childrenToList(listOfLists: ListPerseverance) -> List[List]:
  """
  Converting list[np.ndarray] to list[list].
  """
  for i, innerList in enumerate(listOfLists):
    listOfLists[i] = toList(innerList)

  return listOfLists
