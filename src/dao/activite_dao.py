from business_object.activity_object.abstract_activity import AbstractActivity

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

class ActivityDAO:
    """
    DAO pour la gestion des activités sportives.
    """

    def __init__(self, db: Session):
        """
        Initialise le DAO avec une session SQLAlchemy.
        """
        self.db = db

    def create(self, activite) -> Activity:
        """
        Crée une nouvelle activité pour un utilisateur.
        """

        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_by_id(self, activity_id: int) -> Optional[Activity]:
        """
        Récupère une activité par son ID.
        """
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def get_by_user(self, user_id: int) -> List[Activity]:
        """
        Récupère toutes les activités d'un utilisateur.
        """
        return self.db.query(Activity).filter(Activity.user_id == user_id).all()

    def get_feed(self, user_id: int) -> List[Activity]:
        """
        Récupère le fil d'activités d'un utilisateur (ses activités + celles des utilisateurs qu'il suit).
        """
        # Récupère les IDs des utilisateurs suivis par l'utilisateur
        user_dao = UtilisateurDAO(self.db)  # Supposons que tu as un UtilisateurDAO
        user = user_dao.get(user_id)
        following_ids = user.following + [user_id]  # Ajoute l'utilisateur lui-même

        # Récupère les activités des utilisateurs suivis + les siennes
        return (
            self.db.query(Activity)
            .filter(Activity.user_id.in_(following_ids))
            .order_by(Activity.date.desc())
            .all()
        )

    def get_monthly_activities(self, user_id: int, year: int, month: int) -> List[Activity]:
        """
        Récupère les activités d'un utilisateur pour un mois spécifique.
        """
        return (
            self.db.query(Activity)
            .filter(
                Activity.user_id == user_id,
                Activity.date.extract('year') == year,
                Activity.date.extract('month') == month
            )
            .all()
        )

    def delete(self, activity_id: int) -> bool:
        """
        Supprime une activité par son ID.
        """
        activity = self.get_by_id(activity_id)
        if activity:
            self.db.delete(activity)
            self.db.commit()
            return True
        return False

