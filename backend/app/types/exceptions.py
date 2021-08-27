"""
Custom exceptions collection.
"""


class Error(Exception):
  """Base class for other exceptions"""

  def __init__(self, algorithm, message):
    self.message = f"Error occured while running {algorithm}:\n{message}"
    super().__init__(self.message)


class RuntimeCOVAError(Error):
  """Something went wrong while running COVA"""

  def __init__(self, message):
    super().__init__("COVA", message)


class RuntimeANGELError(Error):
  """Something went wrong while running ANGEL"""

  def __init__(self, message):
    super().__init__("ANGEL", message)
