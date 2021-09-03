"""
Endpoints for ANGEL data collection.
"""
# pylint: disable=R0801

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..dependencies import getDB
from ..types.dataGenerated import ParamsANGEL
from .utils import PARAMS_DO_NOT_EXIST

router = APIRouter(
    prefix="/examples/angel/data",
    tags=["example data ANGEL"],
)


@router.post("/get/{exampleId}",
             summary="Get a sample for given example",
             response_model=schemas.JSONType
             )
def getExampleData(exampleId: int, params: ParamsANGEL, database: Session = Depends(getDB)):
  """
  Returns ANGEL example data.

  Warning: response_model actually returns a DataGenerated object in JSON format
  """
  data = crud.getExampleDataANGEL(database, exampleId, params)
  if data is None:
    raise HTTPException(
        status_code=404, detail=PARAMS_DO_NOT_EXIST)

  return data.jsonData
