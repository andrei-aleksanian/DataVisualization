"""
Endpoints for Examples.
"""
# pylint: disable=R0801
import os
import traceback
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, File, Form, UploadFile
from sqlalchemy.orm import Session
from PIL import Image

from app.visualization.utils.generateCOVA import generateCOVA
from app.visualization.utils.generateANGEL import generateANGEL
from app.visualization.utils.dataGenerated import loadData
from app.types.Custom import DimensionIn
from .utils import saveFile
from ..database import crud, schemas
from ..dependencies import getDB
from ..types.exceptions import RuntimeAlgorithmError, FileConstraintsError
from ..utils.static import staticFolderPath
from ..utils.environment import Env

UNPROCESSABLE_DATASET = "Something went wrong while running the algorithm on your dataset. " +\
    "Please, try a different file"
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

  def cleanSession(exampleId: int = None, imagePath: str = None, error: Exception = None):
    # in case something goes horribly wrong, delete all entries related to example
    if exampleId:
      deleteExampleData(database, exampleId)

    if imagePath:
      os.remove(imagePath)

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(error) if error else UNPROCESSABLE_DATASET
    )

  def saveImage(image: File):
    try:
      imagePath = saveFile(image, staticFolderPath)

      if env in [Env.PRODUCTION.value, Env.DEV.value]:
        img = Image.open(imagePath)
        img = img.resize((700, 400), Image.ANTIALIAS)
        img.save(imagePath, quality=95)
      return imagePath
    except OSError:
      print(traceback.format_exc())
      return cleanSession(imagePath=imagePath)

  def generateData(example: schemas.ExampleCrud, imagePath: str):
    try:
      originalData, labels, scaler = loadData(
          "./app/visualization/Data/bicycle_sample.mat")
      generateCOVA(example.id, example.dimension, originalData, labels, scaler)
      generateANGEL(example.id, example.dimension,
                    originalData, labels, scaler)
    except RuntimeAlgorithmError:
      print(traceback.format_exc())
      cleanSession(example.id, imagePath)
    except FileConstraintsError as error:
      print(traceback.format_exc())
      cleanSession(example.id, imagePath, error)

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
