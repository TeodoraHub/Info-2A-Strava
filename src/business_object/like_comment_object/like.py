from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from business_object.user_object.utilisateur import Utilisateur
from dao.activity_model import ActivityModel

Base = declarative_base()


class Like(Base):
    """Modèle SQLAlchemy pour la table 'liker'"""

    __tablename__ = "liker"

    id_like = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id"), nullable=False)
    date_like = Column(DateTime, nullable=False)

    user = relationship(lambda: Utilisateur, back_populates="likes")
    activite = relationship(lambda: ActivityModel, back_populates="likes")

    def __init__(self, id_user, id_activite, date_like):
        self.id_user = id_user
        self.id_activite = id_activite
        self.date_like = date_like