import logging

from dao.commentaire_dao import CommentaireDAO
from utils.log_decorator import log
from utils.singleton import Singleton


class CommentaireService(metaclass=Singleton):
    """Service pour gérer les opérations liées aux commentaires"""

    def __init__(self):
        self.commentaire_dao = CommentaireDAO()

    @log
    def creer_commentaire(self, id_user: int, id_activite: int, contenu: str) -> bool:
        """Créer un nouveau commentaire

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur qui commente
        id_activite : int
            ID de l'activité
        contenu : str
            Contenu du commentaire

        Returns
        -------
        bool
            True si la création est réussie
        """
        try:
            if not contenu or len(contenu.strip()) == 0:
                logging.warning("Le contenu du commentaire ne peut pas être vide")
                return False

            return self.commentaire_dao.creer_commentaire(id_user, id_activite, contenu)
        except Exception as e:
            logging.error(f"Erreur lors de la création du commentaire: {e}")
            return False

    @log
    def supprimer_commentaire(self, id_comment: int) -> bool:
        """Supprimer un commentaire

        Parameters
        ----------
        id_comment : int
            ID du commentaire

        Returns
        -------
        bool
            True si la suppression est réussie
        """
        try:
            return self.commentaire_dao.supprimer_commentaire(id_comment)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du commentaire: {e}")
            return False

    @log
    def modifier_commentaire(self, id_comment: int, nouveau_contenu: str) -> bool:
        """Modifier un commentaire

        Parameters
        ----------
        id_comment : int
            ID du commentaire
        nouveau_contenu : str
            Nouveau contenu du commentaire

        Returns
        -------
        bool
            True si la modification est réussie
        """
        try:
            if not nouveau_contenu or len(nouveau_contenu.strip()) == 0:
                logging.warning("Le contenu du commentaire ne peut pas être vide")
                return False

            return self.commentaire_dao.modifier_commentaire(id_comment, nouveau_contenu)
        except Exception as e:
            logging.error(f"Erreur lors de la modification du commentaire: {e}")
            return False

    @log
    def get_commentaires_activite(self, id_activite: int):
        """Récupérer tous les commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            ID de l'activité

        Returns
        -------
        list
            Liste des commentaires
        """
        try:
            return self.commentaire_dao.get_commentaires_by_activity(id_activite)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def get_commentaires_user(self, id_user: int):
        """Récupérer tous les commentaires d'un utilisateur

        Parameters
        ----------
        id_user : int
            ID de l'utilisateur

        Returns
        -------
        list
            Liste des commentaires de l'utilisateur
        """
        try:
            return self.commentaire_dao.get_commentaires_by_user(id_user)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def count_commentaires_activite(self, id_activite: int) -> int:
        """Compter le nombre de commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            ID de l'activité

        Returns
        -------
        int
            Nombre de commentaires
        """
        try:
            return self.commentaire_dao.count_commentaires_by_activity(id_activite)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires: {e}")
            return 0
