"""
Schemas or types to be used in the application on different specific events:

1. Read Schemas - e.g. Data or Example.
   This is the data we are expecting to pass the user from teh database.

2. Write Schemas - e.g. DataCreate and ExampleCreate.
   This is teh data we are expecting from the user to write to the database.
"""

# pylint: disable=C0116, C0115

from typing import Optional
from pydantic import BaseModel
from common.types.dataGenerated import ParamsANGEL, ParamsCOVA, JSONType
from common.types.Custom import Dimension


class DataBase(BaseModel):
  """
  Used for reading data records
  """
  jsonData: JSONType


class DataCreateCOVA(DataBase):
  """
  Used for creating COVA data records
  """
  params: ParamsCOVA


class DataCreateANGEL(DataBase):
  """
  Used for creating ANGEL data records
  """
  params: ParamsANGEL


class Data(DataBase):
  id: int
  exampleId: int
  jsonData: JSONType
  exampleName: str

  class Config:
    orm_mode = True


class ExampleBase(BaseModel):
  """
  Used for reading data records
  """
  name: str
  imagePath: str
  description: Optional[str] = None


class ExampleCreate(ExampleBase):
  """
  Used for creating example records
  """
  dimension: Dimension
  originalData: JSONType
  filePath: str
  labels: JSONType


class Example(ExampleBase):
  id: int

  class Config:
    orm_mode = True


class ExampleData(BaseModel):
  originalData: JSONType
  labels: JSONType


class ExampleCrud(Example):
  dimension: Dimension
