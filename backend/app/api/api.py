from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union, NewType
from pydantic import BaseModel, conlist

from data import EXAMPLE_DATA

app = FastAPI()
# CORS from medium
origins = [
    'http://localhost',
    'localhost',
    'http://localhost:3000', # needed for development proxy (React runs at 3000)
    'localhost:3000' 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# My code

data2D = NewType('data2D', List[List[conlist(item_type=float, min_items=2, max_items=2)]])
data3D = NewType('data3D', List[List[conlist(item_type=float, min_items=3, max_items=3)]])

class DataIn(BaseModel):
  data: List[List[float]] # M x N matrix of floats e.g. features of your ML data
  dimension3D: bool = False

class Data(BaseModel):
  data: Union[data2D, data3D]

# COVA endpoints
@app.post("/cova", tags=["COVA"], summary="COVA 2D or 3D dimension shrinking", response_model=Data)
async def index(data: DataIn):
  """
  COVA endpoint accepting data of any number of dimensions and returning 2 or 3.

   - ***dimension3D***: False by default
   - Returns 2D output (N x 2 (float)) if ***dimension3D*** is False
   - Returns 3D output (N x 2 (float)) if ***dimension3D*** is True
  """

  # run my COVA algorithm

  return {"data": [EXAMPLE_DATA]} 



# ANGEL endoints

# TEST endpoints
@app.get("/test")
async def hi():
  return {"Hello": "world"}