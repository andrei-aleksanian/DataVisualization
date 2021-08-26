"""
Endpoints for COVA data collection.
"""
# pylint: disable=R0801

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..dependencies import getDB

router = APIRouter(
    prefix="/examples/angel/data",
    tags=["example data ANGEL"],
)


@router.post("/{exampleId}",
             summary="Add a new ANGEL example data sample to the database")
def createExampleData(
        data: schemas.DataCreateANGEL,
        exampleId: int,
        database: Session = Depends(getDB)):
  """
  Warning: used solely for development

  Accepts new ANGEL data example for specific parameters.
  """
  exampleDb = crud.getExampleDataANGEL(database, exampleId, data.params)
  if exampleDb:
    raise HTTPException(
        status_code=400, detail="A data sample with this param already exists")

  crud.createExampleDataANGEL(database, data, exampleId)
  return Response(status_code=status.HTTP_200_OK)


@router.post("/get/{exampleId}",
             summary="Get all data samples for given example",
             response_model=List[schemas.Data])
def getAllExampleData(exampleId: int, database: Session = Depends(getDB)):
  """
  Warning: used solely for development

  Returns all ANGEL example data.
  """
  return crud.getAllExampleDataANGEL(database, exampleId)
