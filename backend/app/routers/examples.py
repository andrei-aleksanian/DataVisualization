"""
Endpoints for Examples.
"""
# pylint: disable=R0801
import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.visualization.utils.generateCOVA import generateCOVA
from app.visualization.utils.generateANGEL import generateANGEL
from app.types.Custom import DimensionIn
from ..database import crud, schemas
from ..dependencies import getDB
from ..types.exceptions import RuntimeAlgorithmError

UNPROCESSABLE_DATASET = "This data set or image is unprocessable, \
please make sure it is compatible with our application."
EXAMPLE_ALREADY_EXISTS = "An example with this name already exists"

router = APIRouter(
    prefix="/examples",
    tags=["examples"],
)


@router.post("/", summary="Add a new example to the database")
def createExample(
        name: str = Form(...),
        description: Optional[str] = Form(...),
        dimension: DimensionIn = Form(...),
        image: UploadFile = File(...),
        database: Session = Depends(getDB)
):
  """
  Generates a large number of data sets to be viewed in the application for end users.
  Adds the example to the database.
  """

  def cleanSession(exampleId: int, fileName: str = None):
    # in case something goes horribly wrong, delete all entries related to example
    crud.deleteAllExampleDataCOVA(database, exampleId)
    crud.deleteAllExampleDataANGEL(database, exampleId)
    crud.deleteExample(database, exampleId)

    if fileName:
      try:
        os.remove(fileName)
      except OSError as error:
        print(error)

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=UNPROCESSABLE_DATASET
    )

  def saveImage(image: File):
    # Creating the static files directory and saving the image
    fileName = os.getcwd() + "/images/" + image.filename.replace(" ", "-")
    with open(fileName, 'wb+') as file:
      file.write(image.file.read())
      file.close()
    return fileName

  def checkExists(name: str):
    exampleDb = crud.getExampleByName(database, name)
    if exampleDb:
      raise HTTPException(
          status_code=400, detail=EXAMPLE_ALREADY_EXISTS)

  def generateData(example: schemas.ExampleCrud, fileName: str):
    try:
      generateCOVA(example.id, example.dimension)
      generateANGEL(example.id, example.dimension)
    except RuntimeAlgorithmError as exception:
      print(exception)  # need a logger
      cleanSession(example.id, fileName)

  checkExists(name)
  example = crud.createExample(
      database, schemas.ExampleCreate(**{
          "name": name,
          "description": description,
          "dimension": int(dimension),
          "imagePath": image.filename
      })
  )
  fileName = saveImage(image)
  generateData(example, fileName)

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)
