from sqlalchemy import Column, DateTime, Float, Integer, String
from business_object.base import Base


class ActivityModel(Base):
    """Modele ORM unique pour la table des activites persistees."""

    __tablename__ = "activite"

    id = Column("id_activite", Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    description = Column(String)
    sport = Column(String, nullable=False)
    detail_sport = Column(String)
    date_activite = Column(DateTime, nullable=False)
    lieu = Column(String)
    distance = Column(Float, nullable=False)
    duree = Column(Float, nullable=True)  # heures
    id_user = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Activity id={self.id} sport={self.sport} user={self.id_user}>"
