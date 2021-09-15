"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
import numpy as np
from sklearn import preprocessing
from app.database.database import SessionLocal
from app.database.crud import createExampleDataCOVA
from app.database.schemas import DataCreateCOVA
from app.visualization.Cova import runCOVA
from app.types.dataGenerated import ParamsCOVA,\
    CONSTRAINED_NEIGHBOUR,\
    CONSTRAINED_ALPHA,\
    CONSTRAINED_IS_COHORT_NUMBER_ORIGINAL
from app.types.exceptions import RuntimeAlgorithmError
from app.types.Custom import Dimension
from app.utils.environment import Env

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
