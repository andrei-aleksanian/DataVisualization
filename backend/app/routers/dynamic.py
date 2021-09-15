"""
Endpoints for dynamic data fetching.

Used for both COVA and ANGEL. Each has an init function which initializes the cycle.
The dynamic function runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
from any given point in the cycle.
"""
# pylint: disable=R0801, R0913
import os
import traceback
from fastapi import APIRouter, Form, File, UploadFile, HTTPException

from .utils import saveFile, removeFile, validateParamsCOVA
from ..utils.static import tempFolderPath

from ..visualization.Cova import initCOVA, dynamicCOVA
from ..visualization.Angel import initANGEL, dynamicANGEL

from ..types.dataDynamic import DataDynamic, DataDynamicANGEL
from ..types.dataGenerated import ParamsANGEL, ParamsCOVA
from ..types.Custom import DimensionIn
from ..types.exceptions import RuntimeAlgorithmError, FileConstraintsError


router = APIRouter(
    prefix="/dynamic",
    tags=["dynamic"],
)

MAX_ITERATIONS = 10
ITERATIONS_PER_REQUEST = 2
INIT_DATA = {
    # init empty perseverance data
    "prevPartsave": [],
    "prevWrongInHigh": [[]],
    "prevWrongInLow": [[]],
    # init maxiterations and iteration = 0 by default
    "maxIteration": MAX_ITERATIONS,
    "iteration": 0
}


@router.post("/cova-init",
             summary="COVA Demo Dynamic Init",
             response_model=DataDynamic
             )
async def covaDynamicInit(
        neighbourNumber: str = Form(...),
        alpha: float = Form(...),
        isCohortNumberOriginal: bool = Form(...),
        dimension: DimensionIn = Form(...),
        file: UploadFile = File(...)):
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """

  filePath = saveFile(file, tempFolderPath)

  params = ParamsCOVA(**{
      "neighbourNumber": neighbourNumber,
      "alpha": alpha,
      "isCohortNumberOriginal": isCohortNumberOriginal
  })

  initData = None
  try:
    validateParamsCOVA(params)
    initData = initCOVA(params, int(dimension), filePath)
  except RuntimeAlgorithmError as error:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=400, detail=error.message) from error
  except FileConstraintsError as error:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=422, detail=error.message) from error
  finally:
    removeFile(filePath)

  dataDynamic = DataDynamic(**{
      **initData.dict(),
      **INIT_DATA
  })

  return dataDynamic


@router.post("/cova",
             summary="COVA Demo Perseverance",
             response_model=DataDynamic
             )
async def covaDynamic(data: DataDynamic):
  """
  Runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
  from any given point in the cycle.
  """

  dataNew = dynamicCOVA(data, ITERATIONS_PER_REQUEST)
  dataNew.iteration += 1

  return dataNew


@router.post("/angel-init",
             summary="ANGEL Demo Dynamic Init",
             response_model=DataDynamicANGEL
             )
async def angelDynamicInit(
        neighbourNumber: str = Form(...),
        anchorDensity: float = Form(...),
        epsilon: float = Form(...),
        isAnchorModification: bool = Form(...),
        dimension: DimensionIn = Form(...),
        file: UploadFile = File(...)):
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """

  filePath = saveFile(file, tempFolderPath)

  params = ParamsANGEL(**{
      "neighbourNumber": neighbourNumber,
      "anchorDensity": anchorDensity,
      "epsilon": epsilon,
      "isAnchorModification": isAnchorModification
  })

  initData = initANGEL(params, int(dimension), filePath)

  try:
    os.remove(filePath)
  except OSError as error:
    print("Error: %s - %s." % (error.filename, error.strerror))

  dataDynamic = DataDynamicANGEL(**{
      **initData.dict(),
      **INIT_DATA
  })

  return dataDynamic


@router.post("/angel",
             summary="ANGEL Demo Perseverance",
             response_model=DataDynamicANGEL
             )
async def angelDynamic(data: DataDynamicANGEL):
  """
  Runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
  from any given point in the cycle.
  """

  dataNew = dynamicANGEL(data, ITERATIONS_PER_REQUEST)
  dataNew.iteration += 1

  return dataNew
