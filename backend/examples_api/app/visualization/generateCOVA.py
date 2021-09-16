"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
import numpy as np
from sklearn import preprocessing
from common.visualization.Cova import runCOVA
from common.types.dataGenerated import ParamsCOVA,\
    CONSTRAINED_NEIGHBOUR,\
    CONSTRAINED_ALPHA,\
    CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL
from common.types.exceptions import RuntimeAlgorithmError
from common.types.Custom import Dimension
from common.environment import Env
from ..database.database import SessionLocal
from ..database.crud import createExampleDataCOVA
from ..database.schemas import DataCreateCOVA

# Define params and constraints
neighbourNumber = CONSTRAINED_NEIGHBOUR
alpha = CONSTRAINED_ALPHA
isCohortNumberOriginal = CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL

if os.environ.get("ENVIRONMENT") in [Env.TEST.value, Env.DEV.value]:
  neighbourNumber = ['10']
  alpha = [0.4]
  isCohortNumberOriginal = [False]


def generateCOVA(exampleId: int,
                 dimension: Dimension,
                 originalData: np.ndarray,
                 labels: np.ndarray,
                 scaler: preprocessing.MinMaxScaler):
  """
  Genersates all combinations of parameters, runs the COVA algorithm.
  """
  for neighbour in neighbourNumber:
    for alph in alpha:
      for isCohort in isCohortNumberOriginal:
        params = ParamsCOVA(
            neighbourNumber=neighbour,
            alpha=alph,
            isCohortNumberOriginal=isCohort
        )
        try:
          dataGenerated = runCOVA(
              params, dimension, originalData, labels, scaler)
          data = DataCreateCOVA(
              params=params,
              jsonData=dataGenerated.json()
          )

          database = SessionLocal()
          createExampleDataCOVA(database, data, exampleId)
          database.close()
        except Exception as exception:
          raise RuntimeAlgorithmError(f"\n\
              generateCOVA: {exception}\n\
              parameters: neighbourNumber - {neighbour}, \n\
              lambdaParam - {0}, \n\
              alpha - {alph}, \n\
              isCohortNumberOriginal - {isCohort}\n") from exception
