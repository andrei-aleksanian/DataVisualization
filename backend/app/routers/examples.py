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
from ..utils.generateANGEL import generateANGEL
from ..types.exceptions import RuntimeCOVAError, RuntimeANGELError

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
  def doesNameExist():
    exampleDb = crud.getExampleByName(database, example.name)
    if exampleDb:
      raise HTTPException(
          status_code=400, detail=EXAMPLE_ALREADY_EXISTS)

  def cleanSession():
    # in case something goes horribly wrong, delete all entries related to example
    crud.deleteExample(database, example.id)
    crud.deleteAllExampleDataCOVA(database, example.id)

  def generateCOVAData():
    try:
      generateCOVA(example.id)
    except RuntimeCOVAError as errorCOVA:
      cleanSession()
      raise HTTPException(
          status_code=422, detail=UNPROCESSABLE_DATASET) from errorCOVA

  def generateANGELData():
    try:
      generateANGEL(example.id)
    except RuntimeANGELError as errorANGEL:
      cleanSession()
      raise HTTPException(
          status_code=422, detail=UNPROCESSABLE_DATASET) from errorANGEL

  doesNameExist()
  example = crud.createExample(database, example)
  generateCOVAData()
  generateANGELData()

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)
