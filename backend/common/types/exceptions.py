"""
Custom exceptions collection.
"""


class RuntimeAlgorithmError(Exception):
  """Base class for other exceptions"""

  def __init__(self, message):
    self.message = f"Error occured while processing your data: {message}"
    super().__init__(self.message)


class FileConstraintsError(Exception):
  """Base class for other exceptions"""

  def __init__(self, message):
    self.message = f"Error occured while checking your file: {message}"
    super().__init__(self.message)
