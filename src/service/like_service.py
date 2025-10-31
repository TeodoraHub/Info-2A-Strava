import logging

from dao.like_dao import LikeDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class LikeService(metaclass=Singleton):
    """Service pour gérer les opérations liées aux likes"""

    def __init__(self):
        self.like_dao = LikeDAO()

    @log
    def liker_activite(self, id_user: int, id_activite: int) -> bool:
        """Ajouter un like à une activité

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur qui like
        id_activite : int
            ID de l'activité

        Returns
        -------
        bool
            True si le like est ajouté avec succès
        """
        try:
            # Vérifier si l'utilisateur a déjà liké
            if self.like_dao.user_a_like(id_user, id_activite):
                logging.info(f"L'utilisateur {id_user} a déjà liké l'activité {id_activite}")
                return False

            return self.like_dao.creer_like(id_user, id_activite)
        except Exception as e:
            logging.error(f"Erreur lors du like: {e}")
            return False

    @log
    def unliker_activite(self, id_user: int, id_activite: int) -> bool:
        """Retirer un like d'une activité

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur
        id_activite : int
            ID de l'activité

        Returns
        -------
        bool
            True si le like est retiré avec succès
        """
        try:
            return self.like_dao.supprimer_like(id_user, id_activite)
        except Exception as e:
            logging.error(f"Erreur lors du retrait du like: {e}")
            return False

    @log
    def get_likes_activite(self, id_activite: int):
        """Récupérer tous les likes d'une activité

        Parameters
        ----------
        id_activite : int
            ID de l'activité

        Returns
        -------
        list
            Liste des likes
        """
        try:
            return self.like_dao.get_likes_by_activity(id_activite)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des likes: {e}")
            return []

    @log
    def count_likes_activite(self, id_activite: int) -> int:
        """Compter le nombre de likes d'une activité

        Parameters
        ----------
        id_activite : int
            ID de l'activité

        Returns
        -------
        int
            Nombre de likes
        """
        try:
            return self.like_dao.count_likes_by_activity(id_activite)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des likes: {e}")
            return 0

    @log
    def user_a_like(self, id_user: int, id_activite: int) -> bool:
        """Vérifier si un utilisateur a liké une activité

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur
        id_activite : int
            ID de l'activité

        Returns
        -------
        bool
            True si l'utilisateur a liké
        """
        try:
            return self.like_dao.user_a_like(id_user, id_activite)
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du like: {e}")
            return False

    @log
    def get_likes_user(self, id_user: int):
        """Récupérer tous les likes d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        list
            Liste des likes de l'utilisateur
        """
        try:
            return self.like_dao.get_likes_by_user(id_user)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des likes de l'utilisateur: {e}")
            return []
