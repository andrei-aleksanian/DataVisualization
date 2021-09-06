"""
CRUD opertations on the database. To be used and reused many times in the api.

Note: pylint should be disabled for
documentation - all crud operations are self-explanotary.
"""
# pylint: disable=C0116, C0115

from sqlalchemy.orm import Session

from . import schemas
from .models import Examples, ExamplesDataCOVA, ExamplesDataANGEL
from ..types.dataGenerated import ParamsANGEL, ParamsCOVA


def createExample(database: Session, example: schemas.ExampleCreate):
  databaseExample = Examples(**example.dict())
  database.add(databaseExample)
  database.commit()
  database.refresh(databaseExample)
  return databaseExample


def getExample(database: Session, exampleId: int):
  return database.query(Examples).filter(Examples.id == exampleId).first()


def getExampleByName(database: Session, name: str):
  return database.query(Examples).filter(Examples.name == name).first()


def getExamples(database: Session):
  return database.query(
      Examples
  ).all()


def deleteExample(database: Session, exampleId: int):
  database.query(Examples).filter(Examples.id == exampleId).delete()
  database.commit()


def createExampleDataCOVA(database: Session, data: schemas.DataCreateCOVA, exampleId: int):
  params: schemas.ParamsCOVA = data.params
  del data.params
  databaseExampleData = ExamplesDataCOVA(
      **data.dict(), **params.dict(), exampleId=exampleId)
  database.add(databaseExampleData)
  database.commit()
  database.refresh(databaseExampleData)
  return databaseExampleData


def deleteAllExampleDataCOVA(database: Session, exampleId: int):
  database.query(ExamplesDataCOVA).filter(
      ExamplesDataCOVA.exampleId == exampleId).delete()
  database.commit()


def getExampleDataCOVA(database: Session, exampleId: int, params: ParamsCOVA):
  return database.query(
      ExamplesDataCOVA
  ).filter(
      ExamplesDataCOVA.exampleId == exampleId
  ).filter(
      ExamplesDataCOVA.neighbourNumber == params.neighbourNumber
  ).filter(
      ExamplesDataCOVA.lambdaParam == params.lambdaParam
  ).filter(
      ExamplesDataCOVA.isCohortNumberOriginal == params.isCohortNumberOriginal
  ).filter(
      ExamplesDataCOVA.alpha == params.alpha
  ).first()


def getAllExampleDataCOVA(database: Session, exampleId: int):
  return database.query(ExamplesDataCOVA).filter(ExamplesDataCOVA.exampleId == exampleId).all()


def createExampleDataANGEL(database: Session, data: schemas.DataCreateANGEL, exampleId: int):
  params: schemas.ParamsANGEL = data.params
  del data.params
  databaseExampleData = ExamplesDataANGEL(
      **data.dict(), **params.dict(), exampleId=exampleId)
  database.add(databaseExampleData)
  database.commit()
  database.refresh(databaseExampleData)
  return databaseExampleData


def getExampleDataANGEL(database: Session, exampleId: int, params: ParamsANGEL):
  return database.query(
      ExamplesDataANGEL
  ).filter(
      ExamplesDataANGEL.exampleId == exampleId
  ).filter(
      ExamplesDataANGEL.neighbourNumber == params.neighbourNumber
  ).filter(
      ExamplesDataANGEL.lambdaParam == params.lambdaParam
  ).filter(
      ExamplesDataANGEL.anchorDensity == params.anchorDensity
  ).filter(
      ExamplesDataANGEL.epsilon == params.epsilon
  ).filter(
      ExamplesDataANGEL.isAnchorModification == params.isAnchorModification
  ).first()


def getAllExampleDataANGEL(database: Session, exampleId: int):
  return database.query(ExamplesDataANGEL).filter(ExamplesDataANGEL.exampleId == exampleId).all()


def deleteAllExampleDataANGEL(database: Session, exampleId: int):
  database.query(ExamplesDataANGEL).filter(
      ExamplesDataANGEL.exampleId == exampleId).delete()
  database.commit()
