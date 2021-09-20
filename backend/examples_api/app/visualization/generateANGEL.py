"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
import numpy as np
from sklearn import preprocessing
from common.visualization.Angel import runANGEL
from common.types.dataGenerated import ParamsANGEL,\
    CONSTRAINED_ANCHOR_DENSITY,\
    CONSTRAINED_EPSILON,\
    CONSTRAINED_NEIGHBOUR,\
    CONSTRAINED_IS_ANCHOR_MODIFICATION
from common.types.exceptions import RuntimeAlgorithmError
from common.types.Custom import Dimension
from common.environment import Env

from ..database.database import SessionLocal
from ..database.crud import createExampleDataANGEL
from ..database.schemas import DataCreateANGEL

# Define params and constraints
neighbourNumber = CONSTRAINED_NEIGHBOUR
anchorDensity = CONSTRAINED_ANCHOR_DENSITY
epsilon = CONSTRAINED_EPSILON
isAnchorModification = CONSTRAINED_IS_ANCHOR_MODIFICATION


if os.environ.get("ENVIRONMENT") in [Env.TEST.value, Env.DEV.value]:
  neighbourNumber = ['10']
  anchorDensity = [0.1]
  epsilon = [0.1]
  isAnchorModification = [False]


def generateANGEL(exampleId: int,
                  dimension: Dimension,
                  originalData: np.ndarray,
                  labels: np.ndarray,
                  scaler: preprocessing.MinMaxScaler):
  """
  Genersates all combinations of parameters, runs the ANGEL algorithm.
  """
  # pylint: disable=R1702
  for neighbour in neighbourNumber:
    for anchor in anchorDensity:
      for eps in epsilon:
        for anchorMod in isAnchorModification:
          params = ParamsANGEL(
              neighbourNumber=neighbour,
              anchorDensity=anchor,
              epsilon=eps,
              isAnchorModification=anchorMod
          )
          try:
            dataGenerated = runANGEL(
                params, dimension, originalData, labels, scaler)
            data = DataCreateANGEL(
                params=params,
                jsonData=dataGenerated.json()
            )

            database = SessionLocal()
            createExampleDataANGEL(database, data, exampleId)
            database.close()
          except Exception as exception:
            raise RuntimeAlgorithmError(f"\n\
                generateANGEL: {exception}\n\
                parameters: neighbourNumber - {neighbour},\n\
                anchorDensity - {anchor}\n\
                lambdaParam - {0},\n\
                epsilon - {eps},\n\
                isAnchorModification - {anchorMod}\n") from exception
