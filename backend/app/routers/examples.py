"""
Endpoints for Examples.
"""
# pylint: disable=R0801

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..dependencies import getDB
from ..utils.generateCOVA import generateCOVA

router = APIRouter(
    prefix="/examples",
    tags=["examples"],
)


@router.post("/", summary="Add a new example to the database")
def createExample(example: schemas.ExampleCreate, database: Session = Depends(getDB)):
  """
  Generates a large number of data sets to be viewed in the application for end users.
  Adds the example to the database.
  """
  exampleDb = crud.getExampleByName(database, example.name)
  if exampleDb:
    raise HTTPException(
        status_code=400, detail="An example with this name already exists")

  # hardcode params
  # hardcode constraints (for now)

  # COVA
  example = crud.createExample(database, example)

  generateCOVA(example.id)

  # run the hundreds of parameter combinations, store them
  # then store this example in the db - call runCova

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)
