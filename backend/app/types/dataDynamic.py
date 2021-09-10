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
  g: ndarray
  Relation: ndarray
  Ad: ndarray
  alpha: int
  V: ndarray
  labels: ndarray
  points: ndarray


class DataCore(BaseModel):
  """
  Core Data model.
  About to be deprecated and long forgotten
  """
  dimension2D: bool
  points: Points
  labels: List[int]


class DataFormatted(DataCore):
  """
  Data that gets processed in COVA
  """
  g: List
  Relation: List
  Ad: List
  V: List
  alpha: float


class DataDynamic(DataFormatted):
  """
  Data model to be used in demo 2 perseverance
  """
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  iteration: int = 0
  maxIteration: int


# class DataDynamicIn(DataDynamic):
#   dimension: DimensionIn


# class DataDynamicOut(DataDynamic):
#   dimension: Dimension
