"""
Generate all possible combinations of parameters and store them in the Database
"""
from ..database.database import SessionLocal
from ..database.crud import createExampleDataCOVA
from ..database.schemas import DataCreateCOVA
from ..visualization.demo2.COVA import runCOVA
from ..types.dataGenerated import ParamsCOVA

# Define params and constraints
# neighbourNumber = ['10', '20', '30', '10%', '20%', '30%', '40%', '50%']
# lambdaParam = [0, 0.2, 0.4, 0.6, 0.8, 1]
# alpha = [0, 0.2, 0.4, 0.6, 0.8, 1]
# isCohortNumberOriginal = [True, False]

neighbourNumber = ['10']
lambdaParam = [0]
alpha = [0]
isCohortNumberOriginal = [True, False]


def generateCOVA(exampleId: int):
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
          dataGenerated = runCOVA(params)

          data = DataCreateCOVA(
              params=params,
              jsonData=dataGenerated.json()
          )

          database = SessionLocal()
          createExampleDataCOVA(database, data, exampleId)
          database.close()
          # store in db with params
