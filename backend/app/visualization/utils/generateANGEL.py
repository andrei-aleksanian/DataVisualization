"""
Generate all possible combinations of parameters and store them in the Database
"""
import os
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
isAnchorModification = [True, False]

if os.environ.get("ENVIRONMENT") == Env.TEST.value:
  neighbourNumber = ['10']
  lambdaParam = [0]
  anchorDensity = [0.05]
  epsilon = [0.5]
  isAnchorModification = [True]


def generateANGEL(exampleId: int, dimension: Dimension):
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
              dataGenerated = runANGEL(params, dimension)
              data = DataCreateANGEL(
                  params=params,
                  jsonData=dataGenerated.json()
              )

              database = SessionLocal()
              createExampleDataANGEL(database, data, exampleId)
              database.close()
            except Exception as exception:
              raise RuntimeAlgorithmError(f"\
                generateANGEL: {exception}\
                parameters: neighbourNumber - {neighbour}, \
                anchorDensity - {anchor} \
                lambdaParam - {lamb}, \
                epsilon - {eps}, \
                isAnchorModification - {anchorMod}") from exception
