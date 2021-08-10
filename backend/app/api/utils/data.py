"""
Data modification functions to convert data from
COVA and ANGEL into an API-friendly format. (e.g. JSON)
"""
from typing import List, NewType
import numpy as np
from ...types.data import DataOut


def toJSON(result, labels) -> DataOut:
    """
    Convert result and label data to JSON friendly.

    Works for both COVA and ANGEL.
    """
    dimension2D = False
    if result.shape[1] == 2:
        zeros = np.zeros((result.shape[0], 1))
        result = np.hstack((result, zeros))
        dimension2D = True

    return {
        "points": result.tolist(),
        "labels": labels.ravel().tolist(),
        "dimension2D": dimension2D
    }


def toList(numpyArray) -> List:
    """
    Converting np.ndarray to list.
    If np.int64 is passed, [np.int64] is returned.
    """
    if isinstance(numpyArray, np.int64):
        return [numpyArray]

    return numpyArray.tolist()


ListPerservance = NewType('ListPerservance', List[np.ndarray or np.int64])


def childrenToList(listOfLists: ListPerservance) -> List[List]:
    """
    Converting list[np.ndarray] to list[list].
    """
    for i, innerList in enumerate(listOfLists):
        listOfLists[i] = toList(innerList)

    return listOfLists
