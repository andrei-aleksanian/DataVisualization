"""
Types.

Different data types for generated data.
"""
# pylint: disable=C0116, C0115

from typing import List
from pydantic import BaseModel

from .Points import Points


class Params(BaseModel):
  neighbourNumber: int
  lambdaParam: float


class ParamsCOVA(Params):
  alpha: float
  isCohortNumberOriginal: bool


class ParamsANGEL(Params):
  anchorDensity: float
  epsilon: float
  isAnchorModification: bool


class DataGenerated(BaseModel):
  """
  Data model to be used in demo 2 preservation
  """
  prevPartsave: List[int]
  prevWrongInLow: List[List[int]]
  prevWrongInHigh: List[List[int]]
  points: Points
