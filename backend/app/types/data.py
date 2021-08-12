"""
Types.

Different data types to be used accross the application
"""
from typing import List, NewType, TypedDict
from numpy import ndarray
from pydantic import BaseModel, conlist

# There is a flaw here - python can't specify a
# list ending with 0 column
Points = NewType('Points', List[conlist(
    item_type=float, min_items=3, max_items=3)])


class DataNumpy(TypedDict):
  """
  Data that gets processed in COVA
  """
  g: ndarray
  Relation: ndarray
  Ad: ndarray
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


class DataDynamic(DataFormatted):
  """
  Data model to be used in demo 2 perseverance
  """
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  iteration: int = 0
  maxIteration: int
