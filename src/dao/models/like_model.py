from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Import Base from activite_model.py to use the same setup
from dao.models.activite_model import Base


class LikeModel(Base):
    __tablename__ = "like"

    # Primary Key - Note: This isn't strictly necessary for a many-to-many relationship table
    # but is common in SQLAlchemy if you need a unique identifier for the specific 'like' record.
    id_like = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Key to the user who performed the like
    id_user = Column(Integer, ForeignKey("utilisateur.id_user"), nullable=False)

    # Foreign Key to the activity being liked.
    # We use the corrected database column name 'id_activite'
    id_activite = Column(Integer, ForeignKey("activite.id_activite"), nullable=False)

    date_like = Column(DateTime, nullable=False, default=datetime.now)

    # Constraint: A user can only like an activity once
    __table_args__ = (
        UniqueConstraint('id_user', 'id_activite', name='_user_activity_uc'),
    )

    # Relationships
    # Note: Using the actual class names: 'UtilisateurModel' and 'ActivityModel'
    user = relationship("UtilisateurModel", back_populates="likes")
    activity = relationship("ActivityModel", back_populates="likes")