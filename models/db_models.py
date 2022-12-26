from sqlalchemy import Column, Integer, String
from db.database import Base


class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    date = Column(String)
    country = Column(String)