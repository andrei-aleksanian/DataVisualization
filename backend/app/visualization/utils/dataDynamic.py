"""
utils functions for dynamic data loading
"""
from typing import List, NewType
import numpy as np
from sklearn.decomposition import PCA
from app.types.dataDynamic import DataDynamic, DataNumpy, DataFormatted,\
    DataNumpyANGEL, DataFormattedANGEL, DataDynamicANGEL


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
      "points": np.array(previousData.points)
  })


def formatDataIn(previousData: DataDynamic) -> DataNumpy:
  """
  Reformat input data from lists to np.arrays
  """
  if previousData.dimension2D:
    previousData.points = np.delete(previousData.points, 2, 1)

  return DataNumpy(**{
      "alpha": previousData.alpha,
      "points": np.array(previousData.points),
      "originalData": np.array(previousData.originalData),
      "labels": np.array([previousData.labels]),
      "paramRelation": np.array(previousData.paramRelation),
      "paramAd": np.array(previousData.paramAd),
      "paramV": np.array(previousData.paramV),
  })


def formatDimension(points: np.ndarray):
  """Format and return points array."""
  dimension2D = False
  if points.shape[1] == 2:
    zeros = np.zeros((points.shape[0], 1))
    points = np.hstack((points, zeros))
    dimension2D = True

  return points, dimension2D


def formatDataOutANGEL(initData: DataNumpyANGEL) -> DataFormattedANGEL:
  """
  Reformat input data from np.arrays to lists.
  Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
  Only runs once when a request is intialised for ANGEL.
  """
  initData["points"], dimension2D = formatDimension(initData["points"])
  return DataFormattedANGEL(**{
      **initData,
      "anchorPoint": initData["anchorPoint"].tolist(),
      "zParam": initData["zParam"].tolist(),
      "wParam": initData["wParam"].tolist(),
      "originalData": initData["originalData"].tolist(),
      "labels": initData["labels"].ravel().tolist(),
      "points": initData["points"].tolist(),
      "dimension2D": dimension2D,
  })


def formatDataOut(initData: DataNumpy) -> DataFormatted:
  """
  Reformat input data from np.arrays to lists.
  Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
  Only runs once when a request is intialised.
  """
  initData["points"], dimension2D = formatDimension(initData["points"])
  return DataFormatted(**{
      **initData,
      "originalData": initData["originalData"].tolist(),
      "paramRelation": initData["paramRelation"].tolist(),
      "paramAd": initData["paramAd"].tolist(),
      "paramV": initData["paramV"].tolist(),
      "labels": initData["labels"].ravel().tolist(),
      "points": initData["points"].tolist(),
      "dimension2D": dimension2D,
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
