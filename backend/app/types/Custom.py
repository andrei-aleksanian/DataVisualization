"""
Points type.

This type is representing array of 2d and 3d data coordiantes.
"""
from typing import Literal, NewType, List
from pydantic import conlist

# There is a flaw here - python can't specify a
# list ending with 0 column
Points = NewType('Points', List[conlist(
    item_type=float, min_items=3, max_items=3)])

Dimension = Literal[2, 3]
