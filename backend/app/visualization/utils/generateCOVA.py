"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
from app.database.database import SessionLocal
from app.database.crud import createExampleDataCOVA
from app.database.schemas import DataCreateCOVA
from app.visualization.Cova import runCOVA
from app.types.dataGenerated import ParamsCOVA
from app.types.exceptions import RuntimeAlgorithmError
from app.types.Custom import Dimension
from app.utils.environment import Env

# Define params and constraints
neighbourNumber = ['10', '20', '30', '10%', '30%', '50%']
lambdaParam = [0, 0.2, 0.4, 0.6, 0.8, 1]
alpha = [0, 0.2, 0.4, 0.6, 0.8, 1]
isCohortNumberOriginal = [True, False]

if os.environ.get("ENVIRONMENT") == Env.TEST.value:
  neighbourNumber = ['10']
  lambdaParam = [0]
  alpha = [0]
  isCohortNumberOriginal = [True]


def generateCOVA(exampleId: int, dimension: Dimension):
  """
  Genersates all combinations of parameters, runs the COVA algorithm.
  """
  for neighbour in neighbourNumber:
    for lamb in lambdaParam:
      for alph in alpha:
        for isCohort in isCohortNumberOriginal:
          params = ParamsCOVA(
              neighbourNumber=neighbour,
              lambdaParam=lamb,
              alpha=alph,
              isCohortNumberOriginal=isCohort
          )
          try:
            dataGenerated = runCOVA(params, dimension)
            data = DataCreateCOVA(
                params=params,
                jsonData=dataGenerated.json()
            )

            database = SessionLocal()
            createExampleDataCOVA(database, data, exampleId)
            database.close()
          except Exception as exception:
            raise RuntimeAlgorithmError(f"\
              generateCOVA: {exception}\
              parameters: neighbourNumber - {neighbour}, \
              lambdaParam - {lamb}, \
              alpha - {alph}, \
              isCohortNumberOriginal - {isCohort}") from exception
