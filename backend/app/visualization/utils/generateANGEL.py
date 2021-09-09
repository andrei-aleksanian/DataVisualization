"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
import numpy as np
from sklearn import preprocessing
from app.database.database import SessionLocal
from app.database.crud import createExampleDataANGEL
from app.database.schemas import DataCreateANGEL
from app.visualization.Angel import runANGEL
from app.types.dataGenerated import ParamsANGEL
from app.types.exceptions import RuntimeAlgorithmError
from app.types.Custom import Dimension
from app.utils.environment import Env

# Define params and constraints
neighbourNumber = ['10', '20', '30', '10%', '30%', '50%']
lambdaParam = [0, 0.2, 0.4, 0.6, 0.8, 1]
anchorDensity = [0.05, 0.1, 0.2]
epsilon = [0.5, 5]
isAnchorModification = [False, True]

if os.environ.get("ENVIRONMENT") in [Env.TEST.value, Env.DEV.value]:
  neighbourNumber = ['10']
  lambdaParam = [0]
  anchorDensity = [0.05]
  epsilon = [0.5]
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
    for lamb in lambdaParam:
      for anchor in anchorDensity:
        for eps in epsilon:
          for anchorMod in isAnchorModification:
            params = ParamsANGEL(
                neighbourNumber=neighbour,
                lambdaParam=lamb,
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
                lambdaParam - {lamb},\n\
                epsilon - {eps},\n\
                isAnchorModification - {anchorMod}\n") from exception
