"""
utils functions for dynamic data loading

"""
from typing import List, NewType
import numpy as np
# pylint: disable=all
from ...types.data import DataDynamic, DataNumpy, DataFormatted


def formatDataIn(previousData: DataDynamic):
    """
    Reformat input data from lists to np.arrays
    """
    Init = np.array(previousData.points)
    g = np.array(previousData.g)
    label = np.array([previousData.labels])
    Relation = np.array(previousData.Relation)
    Ad = np.array(previousData.Ad)
    V = np.array(previousData.V)

    return Init, g, label, Relation, Ad, V


def formatDataOut(initData: DataNumpy) -> DataFormatted:
    """
    Reformat input data from lnp.arrays to lists.
    Computes wether dimension is 2D or 3D and adds a column of 0s to it if needed.
    """
    dimension2D = False
    if initData["points"].shape[1] == 2:
        zeros = np.zeros((initData["points"].shape[0], 1))
        initData["points"] = np.hstack((initData["points"], zeros))
        dimension2D = True

    return DataFormatted({
        "g": initData["g"].tolist(),
        "Relation": initData["Relation"].tolist(),
        "Ad": initData["Ad"].tolist(),
        "V": initData["V"].tolist(),
        "labels": initData["labels"].ravel().tolist(),
        "points": initData["points"].tolist(),
        "dimension2D": dimension2D
    })


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
