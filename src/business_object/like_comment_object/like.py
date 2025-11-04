from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Like(Base):
    __tablename__ = "liker"  # Nom de la table dans la base de données

    id_like = Column(Integer, primary_key=True, autoincrement=True)  # id du like (clé primaire)
    id_user = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id"), nullable=False)
    date_like = Column(DateTime, nullable=False)

    # Relations (optionnel, à ajuster selon tes besoins)
    user = relationship("Utilisateur", back_populates="likes")
    activite = relationship("Activite", back_populates="likes")

    def __init__(self, id_user, id_activite, date_like):
        self.id_user = id_user
        self.id_activite = id_activite
        self.date_like = date_like
