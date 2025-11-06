from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

Base = declarative_base()


class AbstractActivity(Base):
    __abstract__ = True

    id_activite = Column(Integer, primary_key=True, autoincrement=True, name='id')
    titre = Column(String, nullable=False)
    description = Column(String)
    sport = Column(String, nullable=False)
    date_activite = Column(Date, nullable=False)
    lieu = Column(String)
    distance = Column(Float, nullable=False)
    duree = Column(Float)
    id_user = Column(Integer, ForeignKey('users.id_user'), nullable=False)

    def __init__(self, id_activite, titre, description, sport, date_activite, 
                 lieu, distance, id_user, duree=None):
        self.id_activite = id_activite
        self.titre = titre
        self.description = description
        self.sport = sport
        self.date_activite = date_activite
        self.lieu = lieu
        self.distance = distance
        self.id_user = id_user
        self.duree = duree

    @abstractmethod
    def vitesse(self) -> float:
        pass
