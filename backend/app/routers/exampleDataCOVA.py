"""
Endpoints for ANGEL data collection.
"""
# pylint: disable=R0801
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..types.dataGenerated import ParamsCOVA, DataGeneratedOut
from ..database import crud
from ..dependencies import getDB
from .utils import PARAMS_DO_NOT_EXIST

router = APIRouter(
    prefix="/examples/cova/data",
    tags=["example data COVA"],
)


@router.post("/get/{exampleId}",
             summary="Get a sample for given example",
             response_model=DataGeneratedOut
             )
def getExampleData(exampleId: int, paramsCOVA: ParamsCOVA, database: Session = Depends(getDB)):
  """
  Returns COVA example data.

  Warning: response_model actually returns a DataGenerated object in JSON format
  """
  data = crud.getExampleDataCOVA(database, exampleId, paramsCOVA)
  if data is None:
    raise HTTPException(
        status_code=404, detail=PARAMS_DO_NOT_EXIST)
  return DataGeneratedOut(**{"jsonData": data.jsonData, "exampleName": data.example.name})
