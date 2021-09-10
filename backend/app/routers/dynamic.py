"""
Endpoints for dynamic data fetching.

Used for both COVA and ANGEL. Each has an init function which initializes the cycle.
The dynamic function runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
from any given point in the cycle.
"""
# pylint: disable=R0801, R0913
from fastapi import APIRouter, Form, File, UploadFile

from ..visualization.Cova import initCOVA
from .utils import saveFile

from ..types.dataDynamic import DataDynamic
from ..types.dataGenerated import ParamsCOVA
from ..types.Custom import DimensionIn
from ..utils.static import tempFolderPath

router = APIRouter(
    prefix="/dynamic",
    tags=["dynamic"],
)

MAX_ITERATIONS = 8
ITERATIONS_PER_REQUEST = 2


@router.post("/cova",
             summary="COVA Demo Dynamic Init",
             response_model=DataDynamic
             )
async def covaDynamicInit(
    neighbourNumber: str = Form(...),
    lambdaParam: float = Form(...),
    alpha: float = Form(...),
    isCohortNumberOriginal: bool = Form(...),
    dimension: DimensionIn = Form(...),
    file: UploadFile = File(...),
):
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """

  filePath = saveFile(file, tempFolderPath)

  params = ParamsCOVA(**{
      "neighbourNumber": neighbourNumber,
      "lambdaParam": lambdaParam,
      "alpha": alpha,
      "isCohortNumberOriginal": isCohortNumberOriginal
  })

  initData = initCOVA(params, int(dimension), filePath)

  dataDynamic = DataDynamic(**{
      **initData.dict(),
      # init empty perseverance data
      "prevPartsave": [],
      "prevWrongInHigh": [[]],
      "prevWrongInLow": [[]],
      # init maxiterations and iteration = 0 by default
      "maxIteration": MAX_ITERATIONS,
      "iteration": 0
  })

  return dataDynamic


# @router.post("/cova",
#              summary="COVA Demo Perseverance",
#              response_model=DataDynamic
#              )
# async def covaDynamic(data: DataDynamic):
#   """
#   Runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
#   from any given point in the cycle.
#   """
#   # future note:
#   # check if result has 0s as the last column if user asked for 2d output

#   dataNew = dynamicCOVA(data, ITERATIONS_PER_REQUEST)
#   dataNew.iteration += 1

#   return dataNew
