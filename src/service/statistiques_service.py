import logging
from collections import defaultdict
from datetime import datetime, timedelta

from dao.activite_dao import ActivityDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class StatistiquesService(metaclass=Singleton):
    """Service pour calculer et fournir des statistiques sur les activités"""

    def __init__(self):
        self.activity_dao = ActivityDAO()

    @log
    def get_statistiques_mensuelles(self, id_user: int, year: int = None, month: int = None):
        """Calculer les statistiques mensuelles d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur
        year : int, optional
            Année (par défaut: année courante)
        month : int, optional
            Mois (par défaut: mois courant)

        Returns
        -------
        dict
            Dictionnaire contenant les statistiques mensuelles
        """
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
                "distance_totale": 0,
                "duree_totale": 0,
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0, "duree": 0}),
            }

            for activity in activities:
                # Statistiques globales
                if hasattr(activity, "distance") and activity.distance:
                    stats["distance_totale"] += activity.distance
                if hasattr(activity, "duree") and activity.duree:
                    stats["duree_totale"] += (
                        activity.duree.total_seconds()
                        if hasattr(activity.duree, "total_seconds")
                        else 0
                    )

                # Statistiques par sport
                sport = activity.sport if hasattr(activity, "sport") else "Inconnu"
                stats["par_sport"][sport]["count"] += 1
                if hasattr(activity, "distance") and activity.distance:
                    stats["par_sport"][sport]["distance"] += activity.distance
                if hasattr(activity, "duree") and activity.duree:
                    stats["par_sport"][sport]["duree"] += (
                        activity.duree.total_seconds()
                        if hasattr(activity.duree, "total_seconds")
                        else 0
                    )

            # Convertir defaultdict en dict normal
            stats["par_sport"] = dict(stats["par_sport"])

            return stats
        except Exception as e:
            logging.error(f"Erreur lors du calcul des statistiques mensuelles: {e}")
            return None

    @log
    def get_statistiques_annuelles(self, id_user: int, year: int = None):
        """Calculer les statistiques annuelles d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur
        year : int, optional
            Année (par défaut: année courante)

        Returns
        -------
        dict
            Dictionnaire contenant les statistiques annuelles
        """
        try:
            if year is None:
                year = datetime.now().year

            stats = {
                "year": year,
                "total_activites": 0,
                "distance_totale": 0,
                "duree_totale": 0,
                "par_mois": {},
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0, "duree": 0}),
            }

            for month in range(1, 13):
                monthly_stats = self.get_statistiques_mensuelles(id_user, year, month)
                if monthly_stats:
                    stats["par_mois"][month] = monthly_stats
                    stats["total_activites"] += monthly_stats["total_activites"]
                    stats["distance_totale"] += monthly_stats["distance_totale"]
                    stats["duree_totale"] += monthly_stats["duree_totale"]

                    # Agréger par sport
                    for sport, sport_stats in monthly_stats["par_sport"].items():
                        stats["par_sport"][sport]["count"] += sport_stats["count"]
                        stats["par_sport"][sport]["distance"] += sport_stats["distance"]
                        stats["par_sport"][sport]["duree"] += sport_stats["duree"]

            # Convertir defaultdict en dict normal
            stats["par_sport"] = dict(stats["par_sport"])

            return stats
        except Exception as e:
            logging.error(f"Erreur lors du calcul des statistiques annuelles: {e}")
            return None

    @log
    def get_statistiques_globales(self, id_user: int):
        """Calculer les statistiques globales (toutes périodes confondues)

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        dict
            Dictionnaire contenant les statistiques globales
        """
        try:
            activities = self.activity_dao.get_by_user(id_user)

            stats = {
                "total_activites": len(activities),
                "distance_totale": 0,
                "duree_totale": 0,
                "par_sport": defaultdict(lambda: {"count": 0, "distance": 0, "duree": 0}),
                "premiere_activite": None,
                "derniere_activite": None,
            }

            dates = []
            for activity in activities:
                # Dates
                if hasattr(activity, "date_activite") and activity.date_activite:
                    dates.append(activity.date_activite)

                # Statistiques globales
                if hasattr(activity, "distance") and activity.distance:
                    stats["distance_totale"] += activity.distance
                if hasattr(activity, "duree") and activity.duree:
                    stats["duree_totale"] += (
                        activity.duree.total_seconds()
                        if hasattr(activity.duree, "total_seconds")
                        else 0
                    )

                # Statistiques par sport
                sport = activity.sport if hasattr(activity, "sport") else "Inconnu"
                stats["par_sport"][sport]["count"] += 1
                if hasattr(activity, "distance") and activity.distance:
                    stats["par_sport"][sport]["distance"] += activity.distance
                if hasattr(activity, "duree") and activity.duree:
                    stats["par_sport"][sport]["duree"] += (
                        activity.duree.total_seconds()
                        if hasattr(activity.duree, "total_seconds")
                        else 0
                    )

            # Première et dernière activité
            if dates:
                stats["premiere_activite"] = min(dates)
                stats["derniere_activite"] = max(dates)

            # Convertir defaultdict en dict normal
            stats["par_sport"] = dict(stats["par_sport"])

            return stats
        except Exception as e:
            logging.error(f"Erreur lors du calcul des statistiques globales: {e}")
            return None

    @log
    def get_sport_prefere(self, id_user: int):
        """Déterminer le sport préféré d'un utilisateur (le plus pratiqué)

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        str ou None
            Le sport le plus pratiqué
        """
        try:
            stats = self.get_statistiques_globales(id_user)
            if not stats or not stats["par_sport"]:
                return None

            sport_prefere = max(stats["par_sport"].items(), key=lambda x: x[1]["count"])
            return sport_prefere[0]
        except Exception as e:
            logging.error(f"Erreur lors de la détermination du sport préféré: {e}")
            return None

    @log
    def get_moyenne_par_semaine(self, id_user: int, nb_semaines: int = 4):
        """Calculer les moyennes par semaine sur les N dernières semaines

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur
        nb_semaines : int
            Nombre de semaines à considérer (par défaut: 4)

        Returns
        -------
        dict
            Moyennes par semaine
        """
        try:
            activities = self.activity_dao.get_by_user(id_user)

            # Filtrer sur les N dernières semaines
            now = datetime.now()
            date_limite = now - timedelta(weeks=nb_semaines)

            activities_recentes = [
                a
                for a in activities
                if hasattr(a, "date_activite")
                and a.date_activite
                and a.date_activite >= date_limite
            ]

            total_distance = sum(
                a.distance for a in activities_recentes if hasattr(a, "distance") and a.distance
            )
            total_duree = sum(
                a.duree.total_seconds() if hasattr(a.duree, "total_seconds") else 0
                for a in activities_recentes
                if hasattr(a, "duree") and a.duree
            )

            return {
                "nb_semaines": nb_semaines,
                "activites_par_semaine": len(activities_recentes) / nb_semaines
                if nb_semaines > 0
                else 0,
                "distance_par_semaine": total_distance / nb_semaines if nb_semaines > 0 else 0,
                "duree_par_semaine": total_duree / nb_semaines if nb_semaines > 0 else 0,
            }
        except Exception as e:
            logging.error(f"Erreur lors du calcul des moyennes par semaine: {e}")
            return None
