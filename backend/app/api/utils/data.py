"""
Data modification functions to convert data from
COVA and ANGEL into an API-friendly format. (e.g. JSON)
"""
import numpy as np


def toJSON(result, labels):
  """
  Convert result and label data to JSON friendly.

  Works for both COVA and ANGEL.
  About to be deprecated
  """
  dimension2D = False
  if result.shape[1] == 2:
    zeros = np.zeros((result.shape[0], 1))
    result = np.hstack((result, zeros))
    dimension2D = True

  if labels is None:
    return {
        "points": result.tolist(),
        "dimension2D": dimension2D
    }

  return {
      "points": result.tolist(),
      "labels": labels.ravel().tolist(),
      "dimension2D": dimension2D
  }
