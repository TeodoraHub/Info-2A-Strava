import logging

from dao.suivi_dao import SuiviDAO
from dao.utilisateur_dao import UtilisateurDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class SuiviService(metaclass=Singleton):
    """Service pour gérer les opérations liées aux suivis entre utilisateurs"""

    def __init__(self):
        self.suivi_dao = SuiviDAO()
        self.utilisateur_dao = UtilisateurDAO()

    @log
    def suivre_utilisateur(self, id_suiveur: int, id_suivi: int) -> bool:
        """Faire suivre un utilisateur par un autre

        Parameters
        ----------
        id_suiveur : int
            ID de l'utilisateur qui suit
        id_suivi : int
            ID de l'utilisateur à suivre

        Returns
        -------
        bool
            True si le suivi est créé avec succès
        """
        try:
            # Vérifier que les deux utilisateurs existent
            suiveur = self.utilisateur_dao.trouver_par_id(id_suiveur)
            suivi = self.utilisateur_dao.trouver_par_id(id_suivi)

            if not suiveur or not suivi:
                logging.warning("Un ou plusieurs utilisateurs n'existent pas")
                return False

            # Vérifier si la relation existe déjà
            if self.suivi_dao.user_suit(id_suiveur, id_suivi):
                logging.info(f"L'utilisateur {id_suiveur} suit déjà {id_suivi}")
                return False

            return self.suivi_dao.creer_suivi(id_suiveur, id_suivi)
        except Exception as e:
            logging.error(f"Erreur lors de la création du suivi: {e}")
            return False

    @log
    def ne_plus_suivre(self, id_suiveur: int, id_suivi: int) -> bool:
        """Arrêter de suivre un utilisateur

        Parameters
        ----------
        id_suiveur : int
            ID de l'utilisateur qui suit
        id_suivi : int
            ID de l'utilisateur suivi

        Returns
        -------
        bool
            True si le suivi est supprimé avec succès
        """
        try:
            return self.suivi_dao.supprimer_suivi(id_suiveur, id_suivi)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du suivi: {e}")
            return False

    @log
    def get_followers(self, id_user: int):
        """Récupérer la liste des followers d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        list
            Liste des utilisateurs qui suivent cet utilisateur
        """
        try:
            followers_ids = self.suivi_dao.get_followers(id_user)
            followers = []
            for follower_id in followers_ids:
                follower = self.utilisateur_dao.trouver_par_id(follower_id)
                if follower:
                    followers.append(follower)
            return followers
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des followers: {e}")
            return []

    @log
    def get_following(self, id_user: int):
        """Récupérer la liste des utilisateurs suivis par un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        list
            Liste des utilisateurs suivis
        """
        try:
            following_ids = self.suivi_dao.get_following(id_user)
            following = []
            for following_id in following_ids:
                user = self.utilisateur_dao.trouver_par_id(following_id)
                if user:
                    following.append(user)
            return following
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs suivis: {e}")
            return []

    @log
    def user_suit(self, id_suiveur: int, id_suivi: int) -> bool:
        """Vérifier si un utilisateur en suit un autre

        Parameters
        ----------
        id_suiveur : int
            ID de l'utilisateur qui suit
        id_suivi : int
            ID de l'utilisateur potentiellement suivi

        Returns
        -------
        bool
            True si id_suiveur suit id_suivi
        """
        try:
            return self.suivi_dao.user_suit(id_suiveur, id_suivi)
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du suivi: {e}")
            return False

    @log
    def count_followers(self, id_user: int) -> int:
        """Compter le nombre de followers d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        int
            Nombre de followers
        """
        try:
            return self.suivi_dao.count_followers(id_user)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des followers: {e}")
            return 0

    @log
    def count_following(self, id_user: int) -> int:
        """Compter le nombre d'utilisateurs suivis

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        int
            Nombre d'utilisateurs suivis
        """
        try:
            return self.suivi_dao.count_following(id_user)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des utilisateurs suivis: {e}")
            return 0
