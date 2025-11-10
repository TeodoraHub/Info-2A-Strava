from sqlalchemy import Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ActivityModel(Base):
    __tablename__ = 'activite'

    id = Column('id_activite', Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    sport = Column(String, nullable=False)
    date_activite = Column(Date, nullable=False)
    lieu = Column(String)
    distance = Column(Float, nullable=False)
    duree = Column(Time, nullable=True)
    id_user = Column(Integer, nullable=False)
