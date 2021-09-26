"""
Returning commonly used static folder path
"""
from os import getcwd, path, mkdir
staticFolderPath = getcwd() + "/images/"
tempFolderPath = getcwd() + "/temp/"
generatedDataFolderPath = getcwd() + "/generatedData/"
exampleMatFolderPath = getcwd() + "/exampleMat/"


def createStaticDirectory(folderPath: str):
  """Create the static folder if not exists"""
  if not path.exists(folderPath):
    mkdir(folderPath)
