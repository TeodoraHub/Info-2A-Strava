from sqlalchemy import Column, ForeignKey, Integer
from business_object.base import Base
from sqlalchemy.orm import relationship



class Suivi(Base):
    __tablename__ = "suivi"

    id_suiveur = Column(Integer, ForeignKey("utilisateur.id_user"), primary_key=True)
    id_suivi = Column(Integer, ForeignKey("utilisateur.id_user"), primary_key=True)

    # Relation inverse, pour accéder aux suiveurs d'un utilisateur
    suiveur = relationship("Utilisateur", foreign_keys=[id_suiveur], backref="suivis")
    suivi = relationship("Utilisateur", foreign_keys=[id_suivi], backref="suiveurs")
