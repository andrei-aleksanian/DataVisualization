"""
My API file used for early development.
"""
from os import environ
from concurrent.futures.process import ProcessPoolExecutor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database.database import setUpDatabase
from .routers import dynamic, exampleDataCOVA, exampleDataANGEL, examples
from .utils.static import createStaticDirectory, createTempDirectory
from .utils.environment import Env
from .config import getApp

setUpDatabase()

app = getApp()

createStaticDirectory()
createTempDirectory()
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.on_event("startup")
async def onStartup():
  """Introduce an imitation of an 'event loop'"""
  app.state.executor = ProcessPoolExecutor(max_workers=4)


@app.on_event("shutdown")
async def onShutdown():
  """Stop the 'event loop'"""
  app.state.executor.shutdown()


origins = ['0.0.0.0']
if environ.get("ENVIRONMENT") == Env.DEV.value:
  origins.append('localhost:3000')
  origins.append('http://localhost:3000')

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
