"""
Types.

Different data types for generated data.
"""
# pylint: disable=C0116, C0115

from typing import List, TypedDict, Union, Dict, Any

from pydantic import BaseModel
from numpy import ndarray

from .Custom import Points, Dimension

JSONType = Union[str, int, float, bool,
                 None, Dict[str, Any], List[Any]]


class Params(BaseModel):
  neighbourNumber: str


class ParamsCOVA(Params):
  alpha: float
  isCohortNumberOriginal: bool


class ParamsANGEL(Params):
  anchorDensity: float
  epsilon: float
  isAnchorModification: bool


class DataGeneratedNumpy(TypedDict):
  """
  Data that gets processed in COVA
  """
  originalData: ndarray
  resultData: ndarray
  labels: ndarray
  dimension: Dimension


class DataGenerated(BaseModel):
  """
  Data model to be used in demo 2 preservation
  """
  points: Points
  labels: List[int]
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  dimension2D: bool


class DataGeneratedOut(BaseModel):
  jsonData: JSONType
  exampleName: str
