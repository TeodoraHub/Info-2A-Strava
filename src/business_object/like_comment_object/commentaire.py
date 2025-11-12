from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
    id_utilisateur : int
        Identifiant de l'utilisateur qui commente l'activité
    """

    __tablename__ = "commentaire"

    id_comment = Column(Integer, primary_key=True, autoincrement=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id_activite"), nullable=False)
    contenu = Column(String, nullable=False)
    date_commentaire = Column(DateTime, nullable=False, default=datetime.now)

    # Relations - À L'INTÉRIEUR de la classe
    utilisateur = relationship("Utilisateur", back_populates="commentaires", lazy='joined')
    activite = relationship("Activite", back_populates="commentaires", lazy='joined')

    # Constructeur
    def __init__(self, id_activite, contenu, id_utilisateur, date_commentaire=None, id_comment=None):
        self.id_comment = id_comment
        self.id_activite = id_activite
        self.contenu = contenu
        self.date_commentaire = date_commentaire or datetime.now()
        self.id_utilisateur = id_utilisateur