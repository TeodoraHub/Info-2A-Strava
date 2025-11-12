from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Import Base from activite_model.py to use the same setup
from dao.models.activite_model import Base

class UtilisateurModel(Base):
    # NOTE: The table name must be 'utilisateur' to satisfy FK constraints
    __tablename__ = 'utilisateur'

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    nom_user = Column(String, unique=True, nullable=False)
    mail_user = Column(String, unique=True, nullable=False)
    mdp_hash = Column(String, nullable=False) # Store password hash

    # Relationships
    activities = relationship("ActivityModel", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Commentaire", back_populates="utilisateur", cascade="all, delete-orphan")
    likes = relationship("LikeModel", back_populates="user", cascade="all, delete-orphan")