"""
Data model(table) usikng SQLAlchemy model
"""
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, UniqueConstraint, Boolean, Float
from sqlalchemy.orm import relationship
from .database import Base


class Examples(Base):
  """"
  Examples high level overview data table.

  Includes data reference to the actual data stored in ExamplesData table.
  """
  __tablename__ = "examples"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True)
  description = Column(String)

  dataSamplesCOVA = relationship(
      "ExamplesDataCOVA", back_populates="example")
  dataSamplesANGEL = relationship(
      "ExamplesDataANGEL", back_populates="example")


class ExamplesDataCOVA(Base):
  """"
  ExamplesData stores the data for each example

  Includes data reference to the actual data stored in ExamplesData table.
  """
  __tablename__ = "examplesDataCOVA"
  __table_args__ = (
      UniqueConstraint(
          'neighbourNumber',
          'lambdaParam',
          'alpha',
          'isCohortNumberOriginal'
      ),)

  id = Column(Integer, primary_key=True, index=True)

  neighbourNumber = Column(Integer)
  lambdaParam = Column(Float)
  alpha = Column(Float)
  isCohortNumberOriginal = Column(Boolean)

  jsonData = Column(JSON)

  exampleId = Column(Integer, ForeignKey("examples.id"))
  example = relationship("Examples", back_populates="dataSamplesCOVA")


class ExamplesDataANGEL(Base):
  """"
  ExamplesData stores the data for each example

  Includes data reference to the actual data stored in ExamplesData table.
  """
  __tablename__ = "examplesDataANGEL"
  __table_args__ = (
      UniqueConstraint(
          'neighbourNumber',
          'lambdaParam',
          'anchorDensity',
          'epsilon',
          'isAnchorModification'
      ),)

  id = Column(Integer, primary_key=True, index=True)

  neighbourNumber = Column(Integer)
  lambdaParam = Column(Float)
  anchorDensity = Column(Float)
  epsilon = Column(Float)
  isAnchorModification = Column(Boolean)

  jsonData = Column(JSON)

  exampleId = Column(Integer, ForeignKey("examples.id"))
  example = relationship("Examples", back_populates="dataSamplesANGEL")
