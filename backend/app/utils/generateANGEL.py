"""
Generate all possible combinations of parameters and store them in the Database
"""
# pylint: disable-all
import os
# from ..database.database import SessionLocal
# from ..database.crud import createExampleDataANGEL
# from ..database.schemas import DataCreateANGEL
# from ..visualization.demo2.ANGEL import runANGEL
# from ..types.dataGenerated import ParamsANGEL
from ..types.exceptions import RuntimeANGELError
from .environment import Env

# Define params and constraints
neighbourNumber = ['10', '20', '30', '10%', '30%', '50%']
lambdaParam = [0, 0.2, 0.4, 0.6, 0.8, 1]
alpha = [0, 0.2, 0.4, 0.6, 0.8, 1]
isCohortNumberOriginal = [True, False]

if os.environ.get("ENVIRONMENT") == Env.DEV.value:
  neighbourNumber = ['10']
  lambdaParam = [0]
  alpha = [0]
  isCohortNumberOriginal = [True, False]


def generateANGEL(exampleId: int):
  """
  Genersates all combinations of parameters, runs the ANGEL algorithm.
  """
  for neighbour in neighbourNumber:
    for lamb in lambdaParam:
      for alph in alpha:
        for isCohort in isCohortNumberOriginal:
          try:
            pass
            # TODO finish this
          except Exception as exception:
            raise RuntimeANGELError(f"") from exception
