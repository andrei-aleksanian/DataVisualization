"""
My API file used for early development.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..visualization.demo1.ANGEL import angel
from ..visualization.demo1.COVA import cova
from ..visualization.demo2.COVA import covaPoint
from .utils.data import toJSON, childrenToList

from ..types.data import DataOut, DataOutPerseverance

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

# COVA endpoints


@app.get("/api/cova-demo",
         tags=["COVA"],
         summary="COVA Demo",
         response_model=DataOut)
async def covaDemo():
    """
    Demo endpoint with static output that runs the COVA algorithm.
    Used for early development
    """
    # future note:
    # check if result has 0s as the last column if user asked for 2d output

    result, label = cova()
    return toJSON(result, label)


@app.get("/api/cova-demo-perseverance",
         tags=["COVA"],
         summary="COVA Demo Perseverance",
         response_model=DataOutPerseverance
         )
async def covaDemoPerseverance():
    """
    Demo endpoint with static output that runs the COVA algorithm.
    Used for early development
    """
    # future note:
    # check if result has 0s as the last column if user asked for 2d output

    result, label, prevWrongInHigh, prevWrongInLow, prevPartsave = covaPoint()
    data = toJSON(result, label)

    return {
        "points": data["points"],
        "labels": data["labels"],
        "dimension2D": data["dimension2D"],
        "prevPartsave": prevPartsave,
        "prevWrongInLow": childrenToList(prevWrongInLow),
        "prevWrongInHigh": childrenToList(prevWrongInHigh)
    }

# ANGEL endoints


@ app.get("/api/angel-demo",
          tags=["ANGEL"],
          summary="ANGEL Demo",
          response_model=DataOut)
async def angelDemo():
    """
    Demo endpoint with static output that runs the ANGEL algorithm.
    Used for early development
    """
    # future note:
    # check if result has 0s as the last column if user asked for 2d output

    result, label = angel()
    return toJSON(result, label)
