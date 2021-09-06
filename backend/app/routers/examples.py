"""
Endpoints for Examples.
"""
# pylint: disable=R0801
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, File, Form, UploadFile
from sqlalchemy.orm import Session
from PIL import Image

from app.visualization.utils.generateCOVA import generateCOVA
from app.visualization.utils.generateANGEL import generateANGEL
from app.types.Custom import DimensionIn
from ..database import crud, schemas
from ..dependencies import getDB
from ..types.exceptions import RuntimeAlgorithmError
from ..utils.static import staticFolderPath
from ..utils.environment import Env

UNPROCESSABLE_DATASET = "This data set or image is unprocessable, \
please make sure it is compatible with our application."
EXAMPLE_ALREADY_EXISTS = "An example with this name already exists"
CANNOT_DELETE = "The file cannot be deleted"

env = os.environ.get("ENVIRONMENT")

router = APIRouter(
    prefix="/examples",
    tags=["examples"],
)


def checkExists(database: Session, name: str):
  """Checks example exists and returns an error if not"""
  exampleDb = crud.getExampleByName(database, name)
  if exampleDb:
    raise HTTPException(
        status_code=400, detail=EXAMPLE_ALREADY_EXISTS)


def deleteExampleData(database: Session, exampleId: int):
  """Deletes all related DB data to example"""
  crud.deleteAllExampleDataCOVA(database, exampleId)
  crud.deleteAllExampleDataANGEL(database, exampleId)
  crud.deleteExample(database, exampleId)


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

  def cleanSession(exampleId: int = None, imagePath: str = None):
    # in case something goes horribly wrong, delete all entries related to example
    if exampleId:
      deleteExampleData(database, exampleId)

    if imagePath:
      os.remove(imagePath)

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=UNPROCESSABLE_DATASET
    )

  def saveImage(image: File):
    # Creating the static files directory and saving the image
    try:
      image.filename = str(uuid.uuid4()) + image.filename.replace(" ", "-")
      imagePath = staticFolderPath + image.filename
      with open(imagePath, 'wb+') as file:
        file.write(image.file.read())
        file.close()

      if env in [Env.PRODUCTION.value, Env.DEV.value]:
        img = Image.open(imagePath)
        img = img.resize((700, 400), Image.ANTIALIAS)
        img.save(imagePath, quality=95)
      return imagePath
    except OSError as error:
      print(error)
      return cleanSession(imagePath=imagePath)

  def generateData(example: schemas.ExampleCrud, imagePath: str):
    try:
      generateCOVA(example.id, example.dimension)
      generateANGEL(example.id, example.dimension)
    except RuntimeAlgorithmError as exception:
      print(exception)  # need a logger
      cleanSession(example.id, imagePath)

  checkExists(database, name)
  imagePath = saveImage(image)
  example = crud.createExample(
      database, schemas.ExampleCreate(**{
          "name": name,
          "description": description,
          "dimension": int(dimension),
          "imagePath": image.filename
      })
  )
  generateData(example, imagePath)

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)


@router.delete("/{exampleId}",
               summary="Delete a specific example and the image",
               )
def deleteExample(exampleId: int, database: Session = Depends(getDB)):
  """
  Deletes an example.
  """
  checkExists(database, exampleId)
  example = crud.getExample(database, exampleId)
  os.remove(staticFolderPath + example.imagePath)
  deleteExampleData(database, exampleId)

  return Response(status_code=status.HTTP_200_OK)
