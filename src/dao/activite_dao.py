from typing import List, Optional

from utils.session import Session


class ActivityDAO:
    """
    DAO générique pour toutes les activités dans une table unique.
    La table doit contenir un champ 'type' pour différencier les sous-classes.
    """

    def __init__(self, db: Session, activity_base_cls):
        """
        Initialise le DAO avec une session SQLAlchemy et la classe mappée.

        Parameters
        ----------
        db : Session
            session SQLAlchemy
        activity_base_cls : class
            classe représentant la table des activités
        """
        self.db = db
        self.activity_base_cls = activity_base_cls

    def save(self, activity) -> object:
        """Enregistre une activité dans la base de données."""
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_by_id(self, activity_id: int) -> Optional[object]:
        """Récupère une activité par son ID."""
        return (
            self.db.query(self.activity_base_cls)
            .filter(self.activity_base_cls.id == activity_id)
            .first()
        )

    def get_by_user(self, user_id: int, type_activite: str = None) -> List[object]:
        """Récupère toutes les activités d'un utilisateur, optionnellement filtrées par type."""
        query = self.db.query(self.activity_base_cls).filter(
            self.activity_base_cls.user_id == user_id
        )
        if type_activite:
            query = query.filter(self.activity_base_cls.type == type_activite)
        return query.all()

    def get_feed(self, user_id: int) -> List[object]:
        """Récupère le fil d'activités d'un utilisateur (ses activités + celles des suivis)."""
        from dao.utilisateur_dao import UtilisateurDAO

        user_dao = UtilisateurDAO(self.db)
        user = user_dao.get(user_id)
        following_ids = getattr(user, "following", []) + [user_id]

        return (
            self.db.query(self.activity_base_cls)
            .filter(self.activity_base_cls.user_id.in_(following_ids))
            .order_by(self.activity_base_cls.date_activite.desc())
            .all()
        )

    def get_monthly_activities(
        self, user_id: int, year: int, month: int, type_activite: str = None
    ) -> List[object]:
        """Récupère les activités d'un utilisateur pour un mois spécifique et optionnellement par type."""
        query = self.db.query(self.activity_base_cls).filter(
            self.activity_base_cls.user_id == user_id,
            self.activity_base_cls.date_activite.extract("year") == year,
            self.activity_base_cls.date_activite.extract("month") == month,
        )
        if type_activite:
            query = query.filter(self.activity_base_cls.type == type_activite)
        return query.all()

    def delete(self, activity_id: int) -> bool:
        """Supprime une activité par son ID."""
        activity = self.get_by_id(activity_id)
        if activity:
            self.db.delete(activity)
            self.db.commit()
            return True
        return False
