"""
Endpoints for dynamic data fetching.

Used for both COVA and ANGEL. Each has an init function which initializes the cycle.
The dynamic function runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
from any given point in the cycle.
"""
# pylint: disable=R0801
from fastapi import APIRouter
from ..visualization.Cova import dynamicCOVA, initCOVA

from ..types.dataDynamic import DataDynamic

router = APIRouter(
    prefix="/dynamic",
    tags=["dynamic"],
)

MAX_ITERATIONS = 8
ITERATIONS_PER_REQUEST = 2


@router.get("/cova",
            summary="COVA Demo Dynamic Init",
            response_model=DataDynamic
            )
async def covaDynamicInit():
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """

  initData = initCOVA()

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


@router.post("/cova",
             summary="COVA Demo Perseverance",
             response_model=DataDynamic
             )
async def covaDynamic(data: DataDynamic):
  """
  Runs ITERATIONS_PER_REQUEST amount of cycles of the chosen algorithm
  from any given point in the cycle.
  """
  # future note:
  # check if result has 0s as the last column if user asked for 2d output

  dataNew = dynamicCOVA(data, ITERATIONS_PER_REQUEST)
  dataNew.iteration += 1

  return dataNew
