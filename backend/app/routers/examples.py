"""
Endpoints for Examples.
"""
# pylint: disable=R0801

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.visualization.utils.generateCOVA import generateCOVA
from app.visualization.utils.generateANGEL import generateANGEL
from ..database import crud, schemas
from ..dependencies import getDB
from ..types.exceptions import RuntimeAlgorithmError

UNPROCESSABLE_DATASET = "This data set is unprocessable, \
please make sure it is compatible with our application."
EXAMPLE_ALREADY_EXISTS = "An example with this name already exists"

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

  def cleanSession(exampleId: int):
    # in case something goes horribly wrong, delete all entries related to example
    crud.deleteAllExampleDataCOVA(database, exampleId)
    crud.deleteAllExampleDataANGEL(database, exampleId)
    crud.deleteExample(database, exampleId)
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=UNPROCESSABLE_DATASET
    )

  exampleDb = crud.getExampleByName(database, example.name)
  if exampleDb:
    raise HTTPException(
        status_code=400, detail=EXAMPLE_ALREADY_EXISTS)
  example = crud.createExample(database, example)

  try:
    generateCOVA(example.id, example.dimension)
    generateANGEL(example.id, example.dimension)
  except RuntimeAlgorithmError as exception:
    print(exception)  # need a logger
    cleanSession(example.id)

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)
