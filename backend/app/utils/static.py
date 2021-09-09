"""
Returning commonly used static folder path
"""
from os import getcwd, path, mkdir
staticFolderPath = getcwd() + "/images/"


def createStaticDirectory():
  """Create the static folder if not exists"""
  if not path.exists(staticFolderPath):
    mkdir(staticFolderPath)
