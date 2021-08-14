"""
My API file used for early development.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..visualization.demo1.ANGEL import angel
from ..visualization.demo1.COVA import cova
from ..visualization.demo2.COVA import dynamicCOVA, initCOVA
from .utils.data import toJSON

from ..types.data import DataCore, DataDynamic

app = FastAPI()
# CORS from medium
origins = [
    '0.0.0.0',
    # Dev environment - todo: introduce env variables to take these out in production
    'localhost:3000',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

MAX_ITERATIONS = 8
ITERATIONS_PER_REQUEST = 2

# COVA endpoints


@app.get("/api/cova-demo",
         tags=["COVA"],
         summary="COVA Demo",
         response_model=DataCore)
async def covaDemo():
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """
  # future note:
  # check if result has 0s as the last column if user asked for 2d output

  result, label = cova()
  return toJSON(result, label)


@app.get("/api/cova-demo-dynamic",
         tags=["COVA"],
         summary="COVA Demo Dynamic Init",
         response_model=DataDynamic
         )
async def covaDemoDynamicInit():
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


@app.post("/api/cova-demo-dynamic",
          tags=["COVA"],
          summary="COVA Demo Perseverance",
          response_model=DataDynamic
          )
async def covaDemoDynamic(data: DataDynamic):
  """
  Demo endpoint with static output that runs the COVA algorithm.
  Used for early development
  """
  # future note:
  # check if result has 0s as the last column if user asked for 2d output

  dataNew = dynamicCOVA(data, ITERATIONS_PER_REQUEST)
  dataNew.iteration += 1

  return dataNew

# ANGEL endoints


@app.get("/api/angel-demo",
         tags=["ANGEL"],
         summary="ANGEL Demo",
         response_model=DataCore)
async def angelDemo():
  """
  Demo endpoint with static output that runs the ANGEL algorithm.
  Used for early development
  """
  # future note:
  # check if result has 0s as the last column if user asked for 2d output

  result, label = angel()
  return toJSON(result, label)
