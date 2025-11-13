from __future__ import annotations

from typing import List, Optional, Type

from sqlalchemy import func
from sqlalchemy.orm import Session, sessionmaker

from dao.activity_model import ActivityModel
from dao.db_connection import DBConnection


class ActivityDAO:
    """Operations CRUD sur les activites stockees dans la table `activite`."""

    def __init__(
        self,
        session_factory: sessionmaker | None = None,
        activity_base_cls: Type[ActivityModel] | None = None,
    ):
        connection = DBConnection()
        self._session_factory = session_factory or connection.session_factory
        self._model = activity_base_cls or ActivityModel
        if self._model is None:
            raise ValueError("Une classe de modele d'activite doit etre fournie.")

    def _query(self, session: Session):
        return session.query(self._model)

    def save(self, activity: ActivityModel) -> ActivityModel:
        """Enregistre une activite et renvoie son instance rafraichie."""
        with self._session_factory() as session:
            session.add(activity)
            session.commit()
            session.refresh(activity)
            return activity

    def get_by_id(self, activity_id: int) -> Optional[ActivityModel]:
        """Retourne l'activite identifiee, ou None si absente."""
        with self._session_factory() as session:
            return session.get(self._model, activity_id)

    def get_by_user(
        self, user_id: int, type_activite: Optional[str] = None
    ) -> List[ActivityModel]:
        """Liste les activites d'un utilisateur, optionnellement filtrees par sport."""
        with self._session_factory() as session:
            query = self._query(session).filter(self._model.id_user == user_id)
            if type_activite:
                query = query.filter(self._model.sport == type_activite)
            return query.order_by(self._model.date_activite.desc()).all()

    def get_feed(self, user_id: int) -> List[ActivityModel]:
        """Retourne le fil (utilisateur + suivis)."""
        from dao.suivi_dao import SuiviDAO

        suivi_dao = SuiviDAO(session_factory=self._session_factory)
        following_ids = set(suivi_dao.get_following(user_id))
        following_ids.add(user_id)
        if not following_ids:
            return []

        with self._session_factory() as session:
            return (
                self._query(session)
                .filter(self._model.id_user.in_(following_ids))
                .order_by(self._model.date_activite.desc())
                .all()
            )

    def get_monthly_activities(
        self, user_id: int, year: int, month: int, type_activite: Optional[str] = None
    ) -> List[ActivityModel]:
        """Retourne les activites pour un mois precis."""
        with self._session_factory() as session:
            query = self._query(session).filter(self._model.id_user == user_id)
            query = query.filter(
                func.extract("year", self._model.date_activite) == year,
                func.extract("month", self._model.date_activite) == month,
            )
            if type_activite:
                query = query.filter(self._model.sport == type_activite)
            return query.order_by(self._model.date_activite.desc()).all()

    def delete(self, activity_id: int) -> bool:
        """Supprime une activite par son ID et confirme l'operation."""
        with self._session_factory() as session:
            activity = session.get(self._model, activity_id)
            if activity is None:
                return False
            session.delete(activity)
            session.commit()
            return True
