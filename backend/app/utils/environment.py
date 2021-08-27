"""
Environment variables description
"""
from enum import Enum

# ENVIRONMENT: DEV, TEST, PRODUCTION


class Env(Enum):
  """
  DEV - used for development purposes. e.g. speeding up async functions
  TEST - used solely for testing environments
  PRODUCTION - solely for PRODUCTION deployments
  """
  DEV = "DEV"
  TEST = "TEST"
  PRODUCTION = "PRODUCTION"
