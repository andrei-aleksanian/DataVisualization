"""
Types.

Different data types to be used accross the application
"""
from typing import List, NewType
from pydantic import BaseModel, conlist

# There is a flaw here - python can't specify a
# list ending with 0 column
Points = NewType('Points', List[conlist(
    item_type=float, min_items=3, max_items=3)])


class DataIn(BaseModel):
    """
    DataIn model that we will recieve from the browser
    """
    # M x N matrix of floats e.g. features of your
    # ML data
    data: List[List[float]]
    dimension3D: bool = False


class DataOut(BaseModel):
    """
    Data model to be used to process ANGEL and COVA on the server
    """
    points: Points
    labels: List[int]
