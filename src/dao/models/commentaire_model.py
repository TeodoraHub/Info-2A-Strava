from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Import Base from activite_model.py to use the same setup
from dao.models.activite_model import Base


class Commentaire(Base):
    __tablename__ = "commentaire"

    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)

    # FIX: Corrected Foreign Key to reference the actual database column name
    id_activite = Column(Integer, ForeignKey("activite.id_activite"), nullable=False)

    contenu = Column(String, nullable=False)
    date_commentaire = Column(DateTime, nullable=False, default=datetime.now)

    # Ensure these relationship names (Utilisateur, Activite) match the classes/back_populates used elsewhere
    utilisateur = relationship("UtilisateurModel", back_populates="comments")
    activite = relationship("ActivityModel", back_populates="comments")