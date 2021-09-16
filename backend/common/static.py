"""
Returning commonly used static folder path
"""
from os import getcwd, path, mkdir
staticFolderPath = getcwd() + "/images/"
tempFolderPath = getcwd() + "/temp/"


def createStaticDirectory():
  """Create the static folder if not exists"""
  if not path.exists(staticFolderPath):
    mkdir(staticFolderPath)


def createTempDirectory():
  """Create the static folder if not exists"""
  if not path.exists(tempFolderPath):
    mkdir(tempFolderPath)
