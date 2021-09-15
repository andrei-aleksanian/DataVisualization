"""Application config file"""
import asyncio
from fastapi import FastAPI

app = FastAPI()


def getApp():
  """Return the current application"""
  return app


async def runWithAsync(callback, *args):
  """Imitate an asynchronous process"""
  loop = asyncio.get_event_loop()
  # wait and return result
  return await loop.run_in_executor(app.state.executor, callback, *args)
