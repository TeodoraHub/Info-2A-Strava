from datetime import datetime
from business_object.user_object.utilisateur import Utilisateur

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()  # Définir la base pour tous les modèles SQLAlchemy


class Commentaire(Base):
    """
    Classe représentant un commentaire

    Attributs
    ----------
    id_comment : int
        Identifiant du commentaire
    id_activite : int
        Identifiant de l'activité
    contenu : str
        Contenu du commentaire
    date_commentaire : DateTime
        Date du commentaire
    id_user : int
        Identifiant de l'utilisateur qui commente l'activité
    """

    __tablename__ = "commentaire"  # Nom de la table dans la base de données

    # Définition des colonnes
    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id"), nullable=False)
    contenu = Column(String, nullable=False)
    date_commentaire = Column(DateTime, nullable=False, default=datetime.now)

    # Relations, pour accéder aux objets liés via la clé étrangère
    utilisateur = relationship("Utilisateur", back_populates="commentaires")
    activite = relationship("Activite", back_populates="commentaires")

    # Le constructeur d'origine
    def __init__(self, id_activite, contenu, date_commentaire, id_utilisateur, id_comment=None):
        """Constructeur"""
        self.id_comment = id_comment
        self.id_activite = id_activite
        self.contenu = contenu
        self.date_commentaire = date_commentaire
        self.id_user = id_utilisateur
