"""
Data modification functions to convert data from
COVA and ANGEL into an API-friendly format. (e.g. JSON)
"""

import numpy as np


def to_json(result, labels):
    """
    Convert result and label data to JSON friendly.

    Works for both COVA and ANGEL.
    """
    if result.shape[1] == 2:
        zeros = np.zeros((result.shape[0], 1))
        result = np.hstack((result, zeros))

    return {"points": result.tolist(), "labels": labels.ravel().tolist()}
