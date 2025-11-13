from sqlalchemy import Column, DateTime, ForeignKey, Integer
from business_object.base import Base


class Like(Base):
    __tablename__ = "liker"

    id_like = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)
    id_activite = Column(Integer, ForeignKey("activite.id_activite"), nullable=False)
    date_like = Column(DateTime, nullable=False)

    def __init__(self, id_user, id_activite, date_like):
        self.id_user = id_user
        self.id_activite = id_activite
        self.date_like = date_like
