"""
My API file used for early development.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..angel.ANGEL import angel

from ..types.data import DataOut

app = FastAPI()
# CORS from medium
origins = [
    'http://localhost',
    'localhost',
    # needed for development proxy (React runs at
    # 3000)
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
    """
    Demo endpoint with static output that runs the ANGEL algorithm.
    Used for early development
    """
    # future note:
    # check if result has 0s as the last column if user asked for 2d output

    return angel()
