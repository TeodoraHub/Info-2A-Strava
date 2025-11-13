import logging
from typing import Any, Dict, Optional

from dao.activite_dao import ActivityDAO
from dao.activity_model import ActivityModel
from utils.log_decorator import log
from utils.singleton import Singleton


class ActivityService(metaclass=Singleton):
    """Service gerant les operations liees aux activites."""

    def __init__(self):
        self.activity_dao = ActivityDAO()

    @staticmethod
    def _normalize_duration(value: Any) -> Optional[float]:
        """Transcode divers formats de duree en heures (float)."""
        if value is None:
            return None
        if hasattr(value, "total_seconds"):
            try:
                return round(value.total_seconds() / 3600, 6)
            except Exception:  # pragma: no cover
                return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_detail_sport(activity: Any) -> Optional[str]:
        """Identifie la precision de sport si elle existe sur l'objet metier."""
        for attr in ("detail_sport", "type_velo", "type_nage", "type_terrain"):
            value = getattr(activity, attr, None)
            if value:
                return str(value)
        return None

    def _model_from_mapping(self, payload: Dict[str, Any]) -> ActivityModel:
        return ActivityModel(
            id=payload.get("id_activite"),
            titre=payload["titre"],
            description=payload.get("description"),
            sport=payload["sport"],
            date_activite=payload["date_activite"],
            lieu=payload.get("lieu"),
            distance=float(payload["distance"]),
            duree=self._normalize_duration(payload.get("duree")),
            detail_sport=payload.get("detail_sport"),
            id_user=payload["id_user"],
        )

    @log
    def creer_activite(self, activity) -> bool:
        """Cree une activite a partir d'un business object."""
        activity_data = {
            "titre": activity.titre,
            "description": getattr(activity, "description", None),
            "sport": activity.sport,
            "date_activite": activity.date_activite,
            "lieu": getattr(activity, "lieu", None),
            "distance": getattr(activity, "distance", 0),
            "duree": getattr(activity, "duree", None),
            "id_user": activity.id_user,
            "detail_sport": self._extract_detail_sport(activity),
        }
        if hasattr(activity, "id"):
            activity_data["id_activite"] = getattr(activity, "id")
        elif hasattr(activity, "id_activite"):
            activity_data["id_activite"] = getattr(activity, "id_activite")
        return self.creer_activite_from_dict(activity_data)

    @log
    def creer_activite_from_dict(self, activity_data: Dict[str, Any]) -> bool:
        """Cree une activite a partir d'un dictionnaire."""
        try:
            model = self._model_from_mapping(activity_data)
            return self.activity_dao.save(model) is not None
        except Exception as exc:  # pragma: no cover - log error path
            logging.error(f"Erreur lors de la creation de l'activite: {exc}")
            return False

    @log
    def get_activite_by_id(self, activity_id: int):
        """Recupere une activite par son identifiant."""
        try:
            return self.activity_dao.get_by_id(activity_id)
        except Exception as exc:
            logging.error(f"Erreur lors de la recuperation de l'activite: {exc}")
            return None

    @log
    def get_activites_by_user(self, user_id: int, type_activite: str | None = None):
        """Recupere toutes les activites d'un utilisateur."""
        try:
            return self.activity_dao.get_by_user(user_id, type_activite)
        except Exception as exc:
            logging.error(f"Erreur lors de la recuperation des activites: {exc}")
            return []

    @log
    def get_feed(self, user_id: int):
        """Recupere le fil d'activites de l'utilisateur et de ses suivis."""
        try:
            return self.activity_dao.get_feed(user_id)
        except Exception as exc:
            logging.error(f"Erreur lors de la recuperation du fil: {exc}")
            return []

    @log
    def get_monthly_activities(
        self,
        user_id: int,
        year: int,
        month: int,
        type_activite: str | None = None,
    ):
        """Recupere les activites pour un mois donne."""
        try:
            return self.activity_dao.get_monthly_activities(user_id, year, month, type_activite)
        except Exception as exc:
            logging.error(f"Erreur lors de la recuperation mensuelle: {exc}")
            return []

    @log
    def supprimer_activite(self, activity_id: int) -> bool:
        """Supprime une activite."""
        try:
            return self.activity_dao.delete(activity_id)
        except Exception as exc:
            logging.error(f"Erreur lors de la suppression de l'activite: {exc}")
            return False

    @log
    def modifier_activite(self, activity) -> bool:
        """Remplace une activite existante par la version fournie."""
        try:
            activity_id = getattr(activity, "id", None) or getattr(activity, "id_activite", None)
            if not activity_id:
                logging.warning("Impossible de modifier une activite sans identifiant")
                return False

            payload = {
                "id_activite": activity_id,
                "titre": activity.titre,
                "description": getattr(activity, "description", None),
                "sport": activity.sport,
                "date_activite": activity.date_activite,
                "lieu": getattr(activity, "lieu", None),
                "distance": getattr(activity, "distance", 0),
                "duree": getattr(activity, "duree", None),
                "id_user": activity.id_user,
                "detail_sport": self._extract_detail_sport(activity),
            }
            model = self._model_from_mapping(payload)

            if self.activity_dao.delete(activity_id):
                return self.activity_dao.save(model) is not None
            return False
        except Exception as exc:
            logging.error(f"Erreur lors de la modification de l'activite: {exc}")
            return False

    @log
    def modifier_activite_from_dict(self, activity_data: Dict[str, Any]) -> bool:
        """Modifie une activite a partir d'un dictionnaire."""
        try:
            model = self._model_from_mapping(activity_data)
            activity_id = activity_data.get("id_activite")

            if not activity_id:
                logging.warning("Impossible de modifier une activite sans identifiant")
                return False

            if self.activity_dao.delete(activity_id):
                return self.activity_dao.save(model) is not None
            return False
        except Exception as exc:
            logging.error(f"Erreur lors de la modification de l'activite: {exc}")
            return False
