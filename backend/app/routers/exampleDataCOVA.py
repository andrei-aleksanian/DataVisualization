"""
Endpoints for ANGEL data collection.
"""
# pylint: disable=R0801
from typing import List
from app.types.dataGenerated import ParamsCOVA
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..dependencies import getDB

router = APIRouter(
    prefix="/examples/cova/data",
    tags=["example data COVA"],
)


@router.post("/{exampleId}",
             summary="Add a new COVA example data sample to the database")
def createExampleData(
        data: schemas.DataCreateCOVA,
        exampleId: int,
        database: Session = Depends(getDB)):
  """
  Warning: used solely for development

  Accepts new COVA data example for specific parameters.
  """
  exampleDb = crud.getExampleDataCOVA(database, exampleId, data.params)
  if exampleDb:
    raise HTTPException(
        status_code=400, detail="A data sample with this param already exists")

  crud.createExampleDataCOVA(database, data, exampleId)
  return Response(status_code=status.HTTP_200_OK)


@router.get("/{exampleId}",
            summary="Get all data samples for given example",
            response_model=List[schemas.Data])
def getAllExampleData(exampleId: int, database: Session = Depends(getDB)):
  """
  Warning: used solely for development

  Returns all COVA example data.
  """
  return crud.getAllExampleDataCOVA(database, exampleId)


@router.post("/get/{exampleId}",
             summary="Get a sample for given example",
             )
def getExampleData(exampleId: int, paramsCOVA: ParamsCOVA, database: Session = Depends(getDB)):
  """
  Warning: used solely for development

  Returns all COVA example data.
  """
  data = crud.getExampleDataCOVA(database, exampleId, paramsCOVA).jsonData
  return data
