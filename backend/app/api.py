"""
My API file used for early development.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database.database import setUpDatabase
from .routers import dynamic, exampleDataCOVA, exampleDataANGEL, examples

setUpDatabase()

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

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

app.include_router(dynamic.router, prefix="/api")
app.include_router(examples.router, prefix="/api")
app.include_router(exampleDataCOVA.router, prefix="/api")
app.include_router(exampleDataANGEL.router, prefix="/api")
