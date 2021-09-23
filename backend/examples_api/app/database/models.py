"""
Data model(table) usikng SQLAlchemy model
"""
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, UniqueConstraint, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base


class Examples(Base):
  """"
  Examples high level overview data table.

  Includes data reference to the actual data stored in ExamplesData table.
  """
  __tablename__ = "examples"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(64), unique=True, nullable=False)
  imagePath = Column(String(256), unique=True, nullable=False)
  filePath = Column(String(256), unique=True, nullable=False)
  dimension = Column(Integer, nullable=False)
  description = Column(String(512))
  originalData = Column(JSON)
  labels = Column(JSON)

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
          'alpha',
          'isCohortNumberOriginal',
          'exampleId'
      ),)

  id = Column(Integer, primary_key=True, index=True)

  neighbourNumber = Column(String(4))
  alpha = Column(DECIMAL(2, 1))
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
          'anchorDensity',
          'epsilon',
          'isAnchorModification',
          'exampleId'
      ),)

  id = Column(Integer, primary_key=True, index=True)

  neighbourNumber = Column(String(4))
  anchorDensity = Column(DECIMAL(3, 2))
  epsilon = Column(DECIMAL(2, 1))
  isAnchorModification = Column(Boolean)

  jsonData = Column(JSON)

  exampleId = Column(Integer, ForeignKey("examples.id"))
  example = relationship("Examples", back_populates="dataSamplesANGEL")
