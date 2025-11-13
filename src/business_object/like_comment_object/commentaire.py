from datetime import datetime
from typing import Optional
from business_object.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String





class Commentaire(Base):
    """Modèle ORM pour la table `commentaire`."""

    __tablename__ = "commentaire"

    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id_activite"), nullable=False)
    contenu = Column(String, nullable=False)
    date_comment = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, id_user: int, id_activite: int, contenu: str, date_comment: Optional[datetime] = None):
        self.id_user = id_user
        self.id_activite = id_activite
        self.contenu = contenu
        self.date_comment = date_comment or datetime.now()
