"""
Endpoints for ANGEL data collection.
"""
# pylint: disable=R0801

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.types.dataGenerated import ParamsANGEL, DataGeneratedOut
from common.routers.utils import PARAMS_DO_NOT_EXIST
from ..database import crud
from ..dependencies import getDB

router = APIRouter(
    prefix="/examples/angel/data",
    tags=["example data ANGEL"],
)


@router.post("/get/{exampleId}",
             summary="Get a sample for given example",
             response_model=DataGeneratedOut
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

  return DataGeneratedOut(**{"jsonData": data.jsonData, "exampleName": data.example.name})
