"""
utils functions for dynamic data loading
"""
from typing import List, NewType
import numpy as np
from sklearn.decomposition import PCA
from app.types.dataDynamic import DataDynamic, DataNumpy, DataFormatted


def preserveOrientation(points: np.ndarray, dimension) -> np.ndarray:
  """Rotates the dataset to set it to a ficed orientation. Used after embedding."""
  pca = PCA(n_components=dimension)
  pca.fit(points)
  return pca.transform(points)


def formatDataIn(previousData: DataDynamic) -> DataNumpy:
  """
  Reformat input data from lists to np.arrays
  """
  if previousData.dimension2D:
    previousData.points = np.delete(previousData.points, 2, 1)

  return DataNumpy(**{
      "alpha": previousData.alpha,
      "points": np.array(previousData.points),
      "g": np.array(previousData.g),
      "labels": np.array([previousData.labels]),
      "Relation": np.array(previousData.Relation),
      "Ad": np.array(previousData.Ad),
      "V": np.array(previousData.V),
  })


def formatDimension(points: np.ndarray):
  """Format and return points array."""
  dimension2D = False
  if points.shape[1] == 2:
    zeros = np.zeros((points.shape[0], 1))
    points = np.hstack((points, zeros))
    dimension2D = True

  return points, dimension2D


def formatDataOut(initData: DataNumpy) -> DataFormatted:
  """
  Reformat input data from lnp.arrays to lists.
  Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
  Only runs once when a request is intialised.
  """
  initData["points"], dimension2D = formatDimension(initData["points"])
  return DataFormatted(**{
      **initData,
      "g": initData["g"].tolist(),
      "Relation": initData["Relation"].tolist(),
      "Ad": initData["Ad"].tolist(),
      "V": initData["V"].tolist(),
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
