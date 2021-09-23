"""
utils for routers

e.g. common attributes
"""
import os
import uuid
import traceback
from fastapi import UploadFile, HTTPException

from ..types.dataGenerated import \
    CONSTRAINED_ALPHA,\
    CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL,\
    CONSTRAINED_NEIGHBOUR,\
    CONSTRAINED_IS_ANCHOR_MODIFICATION,\
    CONSTRAINED_EPSILON,\
    CONSTRAINED_ANCHOR_DENSITY_CUSTOM,\
    ParamsCOVA,\
    ParamsANGEL


PARAMS_DO_NOT_EXIST = "The parameters you specified do not point to any specific example."
FILE_COULD_NOT_BE_READ = "Your file can't be read. Please make sure it's in the right format."
FILE_NOT_MAT = "Your file must have the .mat extension."


def getFile(exampleNumber: int):
  """
  DELETE ME - I am a helper method and should not be in production.
  See trello for more details.
  """
  file: str = None
  if exampleNumber == 1:
    file = 'bicycle_sample'
  elif exampleNumber == 2:
    file = 'cylinder_sample'
  elif exampleNumber == 3:
    file = 'flower'
  else:
    raise HTTPException(
        status_code=400, detail="Only 1,2,3 are accepted as exampleNumber")
  return file


def saveFile(file: UploadFile, folderPath: str, image: bool = False):
  """Writing the .mat file to a folder"""
  _, extension = os.path.splitext(file.filename)

  if not image and extension != '.mat':
    raise HTTPException(
        status_code=422, detail=FILE_NOT_MAT)

  try:
    file.filename = str(uuid.uuid4()) + file.filename.replace(" ", "-")
    filePath: str = folderPath + file.filename
    with open(filePath, 'wb+') as fileOpened:
      fileOpened.write(file.file.read())
      fileOpened.close()
  except OSError as error:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=400, detail=FILE_COULD_NOT_BE_READ) from error

  return filePath


def removeFile(filePath: str):
  """Remove a given file and prints an error if something went wrong"""
  try:
    os.remove(filePath)
  except OSError as error:
    print("Error: %s - %s." % (error.filename, error.strerror))


def validateParamsCOVA(params: ParamsCOVA):
  """Validate the input params are within supported bounds"""
  errors = []
  if params.neighbourNumber not in CONSTRAINED_NEIGHBOUR:
    errors.append(
        f"Neighbour number should be one of: {CONSTRAINED_NEIGHBOUR}")
  if params.alpha not in CONSTRAINED_ALPHA:
    errors.append(
        f"Anchor density should be one of: {CONSTRAINED_ALPHA}")
  if params.isCohortNumberOriginal not in CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL:
    errors.append(
        f"Anchor modification should be one of: {CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL}")

  if errors:
    raise HTTPException(
        status_code=422, detail=errors)


def validateParamsANGEL(params: ParamsANGEL):
  """Validate the input params are within supported bounds"""
  errors = []
  if params.neighbourNumber not in CONSTRAINED_NEIGHBOUR:
    errors.append(
        f"Neighbour number should be one of: {CONSTRAINED_NEIGHBOUR}")
  if params.anchorDensity not in CONSTRAINED_ANCHOR_DENSITY_CUSTOM:
    errors.append(
        f"Anchor density should be one of: {CONSTRAINED_ANCHOR_DENSITY_CUSTOM}")
  if params.epsilon not in CONSTRAINED_EPSILON:
    errors.append(
        f"Epsilon should be one of: {CONSTRAINED_EPSILON}")
  if params.isAnchorModification not in CONSTRAINED_IS_ANCHOR_MODIFICATION:
    errors.append(
        f"Anchor modification should be one of: {CONSTRAINED_IS_ANCHOR_MODIFICATION}")

  if errors:
    raise HTTPException(
        status_code=422, detail=errors)
