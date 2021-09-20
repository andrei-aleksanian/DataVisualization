"""
Types.

Different data types to be used accross the application
"""
from typing import List, TypedDict
from numpy import ndarray
from pydantic import BaseModel

# from .Custom import Dimension, DimensionIn, Points
from .Custom import Points


class DataNumpy(TypedDict):
  """
  Data that gets processed in COVA
  """
  originalData: ndarray
  paramRelation: ndarray
  paramAd: ndarray
  alpha: int
  paramV: ndarray
  labels: ndarray
  points: ndarray


class DataNumpyANGEL(TypedDict):
  """
  Data that gets processed in COVA
  """
  anchorPoint: ndarray
  zParam: ndarray
  wParam: ndarray
  paramEps: float
  originalData: ndarray
  labels: ndarray
  points: ndarray


class DataCore(BaseModel):
  """
  Core Data model.
  About to be deprecated and long forgotten
  """
  dimension2D: bool
  points: Points
  originalData: List
  resultData: List
  labels: List[int]


class DataFormatted(DataCore):
  """
  Data that gets processed in COVA
  """
  paramRelation: List
  paramAd: List
  paramV: List
  alpha: float


class DataFormattedANGEL(DataCore):
  """
  Data that gets processed in COVA
  """
  anchorPoint: List
  zParam: List
  wParam: List
  paramEps: float


class DataDynamic(DataFormatted):
  """
  Data model to be used in demo 2 perseverance
  """
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  iteration: int = 0
  maxIteration: int


class DataDynamicANGEL(DataFormattedANGEL):
  """
  Data model to be used in demo 2 perseverance
  """
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  iteration: int = 0
  maxIteration: int
