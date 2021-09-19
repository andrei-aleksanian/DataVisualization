"""
My API file used for early development.
"""
from os import environ
from concurrent.futures.process import ProcessPoolExecutor
from fastapi.middleware.cors import CORSMiddleware
from common.static import createTempDirectory
from common.environment import Env
from common.config import getApp
from .routers import dynamic


app = getApp()

createTempDirectory()


@app.on_event("startup")
async def onStartup():
  """Introduce an imitation of an 'event loop'"""
  app.state.executor = ProcessPoolExecutor()


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
