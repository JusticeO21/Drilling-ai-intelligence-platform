from sqlalchemy import Column, Integer, String, Float
from common.database import Base


class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    depth = Column(Float)
