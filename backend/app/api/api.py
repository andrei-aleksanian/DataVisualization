"""
My API file used for early development.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..angel.ANGEL import angel

from ..types.data import DataOut, DataIn
from data import EXAMPLE_DATA

app = FastAPI()
# CORS from medium
origins = [
    'http://localhost',
    'localhost',
    # needed for development proxy (React runs at 3000)
    'http://localhost:3000',
    'localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# COVA endpoints


# ANGEL endoints


@app.get("/angel-demo",
         tags=["ANGEL"],
         summary="ANGEL Demo",
         response_model=DataOut)
async def angel_demo():
  # run the algorithm on sample data from jupyter

  return angel()
