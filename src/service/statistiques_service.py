import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from dao.activite_dao import ActivityDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class StatistiquesService(metaclass=Singleton):
    """Calcule des statistiques agregees sur les activites stockees."""

    def __init__(self):
        self.activity_dao = ActivityDAO()

    @staticmethod
    def _distance_km(activity) -> float:
        value = getattr(activity, "distance", 0) or 0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _duree_heures(activity) -> float:
        value = getattr(activity, "duree", None)
        if value is None:
            return 0.0
        if hasattr(value, "total_seconds"):
            try:
                return float(value.total_seconds()) / 3600
            except Exception:  # pragma: no cover
                return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _sport(activity) -> str:
        return getattr(activity, "sport", "inconnu") or "inconnu"

    def _aggregate(self, activities) -> Dict[str, Dict[str, float]]:
        data = defaultdict(lambda: {"count": 0, "distance": 0.0, "duree": 0.0})
        for activity in activities:
            sport = self._sport(activity)
            distance = self._distance_km(activity)
            duree = self._duree_heures(activity)
            bucket = data[sport]
            bucket["count"] += 1
            bucket["distance"] += distance
            bucket["duree"] += duree
        return data

    @log
    def get_statistiques_mensuelles(
        self, id_user: int, year: Optional[int] = None, month: Optional[int] = None
    ):
        """Retourne les stats pour un mois."""
        try:
            if year is None or month is None:
                now = datetime.now()
                year = year or now.year
                month = month or now.month

            activities = self.activity_dao.get_monthly_activities(id_user, year, month)
            stats = {
                "year": year,
                "month": month,
                "total_activites": len(activities),
                "distance_totale": 0.0,
                "duree_totale": 0.0,
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0.0, "duree": 0.0}),
            }

            aggregated = self._aggregate(activities)
            for sport, values in aggregated.items():
                stats["par_sport"][sport]["count"] = values["count"]
                stats["par_sport"][sport]["distance"] = values["distance"]
                stats["par_sport"][sport]["duree"] = values["duree"]
                stats["distance_totale"] += values["distance"]
                stats["duree_totale"] += values["duree"]

            stats["par_sport"] = dict(stats["par_sport"])
            return stats
        except Exception as exc:
            logging.error(f"Erreur lors du calcul des statistiques mensuelles: {exc}")
            return None

    @log
    def get_statistiques_annuelles(self, id_user: int, year: Optional[int] = None):
        """Retourne les stats agregees sur 12 mois."""
        try:
            year = year or datetime.now().year
            stats = {
                "year": year,
                "total_activites": 0,
                "distance_totale": 0.0,
                "duree_totale": 0.0,
                "par_mois": {},
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0.0, "duree": 0.0}),
            }

            for month in range(1, 13):
                monthly = self.get_statistiques_mensuelles(id_user, year, month)
                if not monthly:
                    continue
                stats["par_mois"][month] = monthly
                stats["total_activites"] += monthly["total_activites"]
                stats["distance_totale"] += monthly["distance_totale"]
                stats["duree_totale"] += monthly["duree_totale"]

                for sport, values in monthly["par_sport"].items():
                    stats["par_sport"][sport]["count"] += values["count"]
                    stats["par_sport"][sport]["distance"] += values["distance"]
                    stats["par_sport"][sport]["duree"] += values["duree"]

            stats["par_sport"] = dict(stats["par_sport"])
            return stats
        except Exception as exc:
            logging.error(f"Erreur lors du calcul des statistiques annuelles: {exc}")
            return None

    @log
    def get_statistiques_globales(self, id_user: int):
        """Retourne les stats globales (toute l'historique)."""
        try:
            activities = self.activity_dao.get_by_user(id_user)
            stats = {
                "total_activites": len(activities),
                "distance_totale": 0.0,
                "duree_totale": 0.0,
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0.0, "duree": 0.0}),
                "premiere_activite": None,
                "derniere_activite": None,
            }

            aggregated = self._aggregate(activities)
            for sport, values in aggregated.items():
                stats["par_sport"][sport] = values
                stats["distance_totale"] += values["distance"]
                stats["duree_totale"] += values["duree"]

            if activities:
                dates = [
                    a.date_activite for a in activities if getattr(a, "date_activite", None)
                ]
                if dates:
                    stats["premiere_activite"] = min(dates)
                    stats["derniere_activite"] = max(dates)

            stats["par_sport"] = dict(stats["par_sport"])
            return stats
        except Exception as exc:
            logging.error(f"Erreur lors du calcul des statistiques globales: {exc}")
            return None

    @log
    def get_sport_prefere(self, id_user: int) -> Optional[str]:
        """Retourne le sport le plus pratique."""
        try:
            stats = self.get_statistiques_globales(id_user)
            if not stats or not stats["par_sport"]:
                return None
            return max(
                stats["par_sport"].items(),
                key=lambda item: item[1]["count"],
            )[0]
        except Exception as exc:
            logging.error(f"Erreur lors de la determination du sport prefere: {exc}")
            return None

    @log
    def get_moyenne_par_semaine(self, id_user: int, nb_semaines: int = 4):
        """Calcule les moyennes hebdomadaires sur les N dernieres semaines."""
        try:
            activities = self.activity_dao.get_by_user(id_user)
            if nb_semaines <= 0:
                return {"nb_semaines": 0, "activites_par_semaine": 0, "distance_par_semaine": 0, "duree_par_semaine": 0}

            now = datetime.now()
            date_limite = now - timedelta(weeks=nb_semaines)
            recentes = [
                a
                for a in activities
                if getattr(a, "date_activite", None) and a.date_activite >= date_limite
            ]

            total_distance = sum(self._distance_km(a) for a in recentes)
            total_duree = sum(self._duree_heures(a) for a in recentes)

            return {
                "nb_semaines": nb_semaines,
                "activites_par_semaine": len(recentes) / nb_semaines,
                "distance_par_semaine": total_distance / nb_semaines,
                "duree_par_semaine": total_duree / nb_semaines,
            }
        except Exception as exc:
            logging.error(f"Erreur lors du calcul des moyennes par semaine: {exc}")
            return None
