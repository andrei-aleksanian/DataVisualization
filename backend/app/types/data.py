from pydantic import BaseModel, conlist
from typing import List, Union, NewType

Data2D = NewType(
    'Data2D', List[conlist(item_type=float, min_items=2, max_items=2)])
Data3D = NewType(
    'Data3D', List[conlist(item_type=float, min_items=3, max_items=3)])


class DataIn(BaseModel):
  """
  DataIn model that we will recieve from the browser
  """
  # M x N matrix of floats e.g. features of your ML data
  data: List[List[float]]
  dimension3D: bool = False


class DataOut(BaseModel):
  """
  Data model to be used to process ANGEL and COVA on the server
  """
  points: Union[Data2D, Data3D]
  labels: List[int]
