import logging

from dao.activite_dao import ActivityDAO
from dao.suivi_dao import SuiviDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class ActivityService(metaclass=Singleton):
    """Service pour gérer les opérations liées aux activités"""

    def __init__(self):
        self.suivi_dao = SuiviDAO()
        self.activity_dao = ActivityDAO()

    @log
    def creer_activite(self, activity) -> bool:
        """Créer une nouvelle activité

        Parameters
        ----------
        activity : AbstractActivity
            l'activité à créer

        Returns
        -------
        bool
            True si la création est réussie
        """
        try:
            result = self.activity_dao.save(activity)
            return result is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'activité: {e}")
            return False

    @log
    def get_activite_by_id(self, activity_id: int):
        """Récupérer une activité par son ID

        Parameters
        ----------
        activity_id : int
            ID de l'activité

        Returns
        -------
        AbstractActivity ou None
        """
        try:
            return self.activity_dao.get_by_id(activity_id)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'activité: {e}")
            return None

    @log
    def get_activites_by_user(self, user_id: int, type_activite: str = None):
        """Récupérer toutes les activités d'un utilisateur

        Parameters
        ----------
        user_id : int
            ID de l'utilisateur
        type_activite : str, optional
            Type d'activité à filtrer

        Returns
        -------
        list
            Liste des activités
        """
        try:
            return self.activity_dao.get_by_user(user_id, type_activite)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des activités: {e}")
            return []

    @log
    def get_feed(self, user_id: int):
        """Récupérer le fil d'actualités d'un utilisateur
        (ses activités + celles des personnes qu'il suit)

        Parameters
        ----------
        user_id : int
            ID de l'utilisateur

        Returns
        -------
        list
            Liste des activités du fil
        """
        try:
            return self.activity_dao.get_feed(user_id)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du fil d'actualités: {e}")
            return []

    @log
    def get_monthly_activities(
        self, user_id: int, year: int, month: int, type_activite: str = None
    ):
        """Récupérer les activités d'un utilisateur pour un mois donné

        Parameters
        ----------
        user_id : int
            ID de l'utilisateur
        year : int
            Année
        month : int
            Mois (1-12)
        type_activite : str, optional
            Type d'activité à filtrer

        Returns
        -------
        list
            Liste des activités du mois
        """
        try:
            return self.activity_dao.get_monthly_activities(user_id, year, month, type_activite)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des activités mensuelles: {e}")
            return []

    @log
    def supprimer_activite(self, activity_id: int) -> bool:
        """Supprimer une activité

        Parameters
        ----------
        activity_id : int
            ID de l'activité à supprimer

        Returns
        -------
        bool
            True si la suppression est réussie
        """
        try:
            return self.activity_dao.delete(activity_id)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'activité: {e}")
            return False

    @log
    def modifier_activite(self, activity) -> bool:
        """Modifier une activité existante

        Parameters
        ----------
        activity : AbstractActivity
            l'activité avec les modifications

        Returns
        -------
        bool
            True si la modification est réussie
        """
        try:
            # Suppression puis recréation (selon la logique de votre DAO)
            if self.activity_dao.delete(activity.id):
                result = self.activity_dao.save(activity)
                return result is not None
            return False
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'activité: {e}")
            return False
