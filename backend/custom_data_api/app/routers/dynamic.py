"""
Endpoints for dynamic data fetching.

Used for both COVA and ANGEL. Each has an init function which initializes the cycle.
The dynamic function runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
from any given point in the cycle.
"""
# pylint: disable=R0801, R0913
import traceback
from fastapi import APIRouter, Form, File, UploadFile, HTTPException

from common.routers.utils import saveFile, removeFile, validateParamsCOVA, validateParamsANGEL
from common.static import tempFolderPath
from common.config import runWithAsync

from common.visualization.Cova import initCOVA, dynamicCOVA
from common.visualization.Angel import initANGEL, dynamicANGEL

from common.types.dataDynamic import DataDynamic, DataFormatted,\
    DataDynamicANGEL, DataFormattedANGEL
from common.types.dataGenerated import ParamsANGEL, ParamsCOVA
from common.types.Custom import DimensionIn
from common.types.exceptions import RuntimeAlgorithmError, FileConstraintsError


router = APIRouter(
    prefix="/dynamic",
    tags=["dynamic"],
)

MAX_ITERATIONS = 10
ITERATIONS_PER_REQUEST = 2


def getInitData(angel: bool = False):
  """Return initial data."""
  return {
      # init empty perseverance data
      "prevPartsave": [],
      "prevWrongInHigh": [[]],
      "prevWrongInLow": [[]],
      # init maxiterations and iteration = 0 by default
      "maxIteration": 1 if angel else MAX_ITERATIONS,
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

  initData: DataFormatted = None
  try:
    validateParamsCOVA(params)
    initData = await runWithAsync(initCOVA, params, int(dimension), filePath)
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
      **getInitData()
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
  dataNew: DataDynamic = None
  try:
    dataNew = await runWithAsync(dynamicCOVA, data, ITERATIONS_PER_REQUEST)
    dataNew.iteration += 1
  except RuntimeAlgorithmError as error:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=400, detail=error.message) from error

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

  initData: DataFormattedANGEL = None
  try:
    validateParamsANGEL(params)
    initData = await runWithAsync(initANGEL, params, int(dimension), filePath)
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

  dataDynamic = DataDynamicANGEL(**{
      **initData.dict(),
      **getInitData(True)
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
  dataNew: DataDynamicANGEL = None
  try:
    dataNew = await runWithAsync(dynamicANGEL, data, MAX_ITERATIONS * ITERATIONS_PER_REQUEST)
    dataNew.iteration += 1
  except RuntimeAlgorithmError as error:
    print(traceback.format_exc())
    raise HTTPException(
        status_code=400, detail=error.message) from error

  return dataNew
