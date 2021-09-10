"""
utils for routers

e.g. common attributes
"""
import uuid
from fastapi import File


PARAMS_DO_NOT_EXIST = "The parameters you specified do not point to any specific example"


def saveFile(file: File, folderPath: str):
  """Writing the file to a folder"""
  file.filename = str(uuid.uuid4()) + file.filename.replace(" ", "-")
  filePath: str = folderPath + file.filename
  with open(filePath, 'wb+') as fileOpened:
    fileOpened.write(file.file.read())
    fileOpened.close()

  return filePath
