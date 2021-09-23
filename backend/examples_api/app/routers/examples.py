"""
Endpoints for Examples.
"""
# pylint: disable=R0801, too-many-arguments, too-many-locals
import os
import json
import traceback
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, File, Form, UploadFile
from numpy import ndarray
from sqlalchemy.orm import Session
from PIL import Image
from sklearn.preprocessing import MinMaxScaler

from common.visualization.utils.dataGenerated import checkDimension, loadData
from common.visualization.lib.FunctionFile import postProcessing
from common.types.Custom import DimensionIn
from common.routers.utils import saveFile
from common.types.exceptions import RuntimeAlgorithmError, FileConstraintsError
from common.static import staticFolderPath, generatedDataFolderPath
from common.environment import Env
from ..visualization.generateCOVA import generateCOVA
from ..visualization.generateANGEL import generateANGEL
from ..database import crud, schemas
from ..dependencies import getDB


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
        file: UploadFile = File(...),
        database: Session = Depends(getDB)
):
  """
  Generates a large number of data sets to be viewed in the application for end users.
  Adds the example to the database.
  """

  def cleanSession(
      exampleId: int = None,
      imagePath: str = None,
      filePath: str = None,
      error: Exception = None
  ):
    # in case something goes horribly wrong, delete all entries related to example
    if exampleId:
      deleteExampleData(database, exampleId)

    if imagePath:
      os.remove(imagePath)

    if filePath:
      os.remove(filePath)

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(error) if error else UNPROCESSABLE_DATASET
    )

  def saveImage(image: File):
    try:
      imagePath = saveFile(image, staticFolderPath, image=True)

      if env in [Env.PRODUCTION.value, Env.DEV.value]:
        img = Image.open(imagePath)
        img = img.resize((700, 400), Image.ANTIALIAS)
        img.save(imagePath, quality=95)
      return imagePath
    except OSError:
      print(traceback.format_exc())
      return cleanSession(imagePath=imagePath)

  def generateData(
          example: schemas.ExampleCrud,
          imagePath: str,
          filePath: str,
          originalData: ndarray,
          labels: ndarray,
          scaler: MinMaxScaler
  ):
    try:
      generateCOVA(example.id, example.dimension, originalData, labels, scaler)
      generateANGEL(example.id, example.dimension,
                    originalData, labels, scaler)
    except RuntimeAlgorithmError:
      cleanSession(example.id, imagePath=imagePath, filePath=filePath)
    finally:
      print(traceback.format_exc())

  def readData(filePath: str, imagePath: str):
    try:
      return loadData(filePath)
    except FileConstraintsError as error:
      return cleanSession(example.id, imagePath, filePath, error)
    except FileNotFoundError as error:
      return cleanSession(example.id, imagePath, filePath, error)
    finally:
      print(traceback.format_exc())

  checkExists(database, name)
  filePath = saveFile(file, generatedDataFolderPath)
  imagePath = saveImage(image)
  originalData, labels, scaler = readData(filePath, imagePath)
  dimensionOriginal = originalData.shape[1]
  originalData = postProcessing(originalData, dimensionOriginal)
  originalData = checkDimension(originalData, dimensionOriginal)
  example = crud.createExample(
      database, schemas.ExampleCreate(**{
          "name": name,
          "description": description,
          "dimension": int(dimension),
          "imagePath": image.filename,
          "filePath": file.filename,
          "originalData": json.dumps(originalData.tolist()),
          "labels": json.dumps(labels.ravel().tolist())
      })
  )
  generateData(example, imagePath, filePath, originalData, labels, scaler)

  return Response(status_code=status.HTTP_200_OK)


@router.get("/",
            summary="Get all available examples stored in the database",
            response_model=List[schemas.Example])
def getAllExamples(database: Session = Depends(getDB)):
  """
  Returns all examples without the related data.
  """
  return crud.getExamples(database)


@router.get("/{exampleId}",
            summary="Get an available example originalData and labels stored in the database",
            response_model=schemas.ExampleData)
def getExample(exampleId: int, database: Session = Depends(getDB)):
  """
  Returns example originalData and labels
  """
  example = crud.getExample(database, exampleId)
  if not example:
    raise HTTPException(status_code=404)

  dimension2D = True
  for point in json.loads(example.originalData):
    if not point[2] == 0:
      dimension2D = False
  return schemas.ExampleData(**{
      "originalData": example.originalData,
      "labels": example.labels,
      "dimension2D": dimension2D,
      "exampleName": example.name
  })


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
