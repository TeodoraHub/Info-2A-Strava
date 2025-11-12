from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AbstractActivity(Base):
    __tablename__ = "activite"  # une seule table pour tout
    id_activite = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    sport = Column(String, nullable=False)
    date_activite = Column(Date, nullable=False)
    lieu = Column(String)
    distance = Column(Float, nullable=False)
    duree = Column(Float)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)  # assumes table users

    __mapper_args__ = {
        'polymorphic_on': sport,
        'polymorphic_identity': 'abstract_activity'
    }

    def vitesse(self) -> float:
        raise NotImplementedError("Chaque sous-classe doit définir sa méthode vitesse")
