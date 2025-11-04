import logging
from datetime import datetime

from business_object.like_comment_object.like import Like
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class LikeDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Likes de la base de données via SQLAlchemy"""

    def __init__(self):
        """Initialise la classe avec la session SQLAlchemy récupérée depuis DBConnection.

        La session est utilisée pour interagir avec la base de données.
        """
        self.session = DBConnection().session  # Récupère la session SQLAlchemy depuis DBConnection

    @log
    def creer_like(self, id_user, id_activite) -> bool:
        """Création d'un like dans la base de données.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur qui aime l'activité.
        id_activite : int
            Identifiant de l'activité aimée.

        Returns
        -------
        bool
            True si le like a été créé avec succès, False en cas d'erreur.
        """
        try:
            new_like = Like(id_user=id_user, id_activite=id_activite, date_like=datetime.now())
            self.session.add(new_like)
            self.session.commit()
            return True
        except Exception as e:
            logging.info(e)
            self.session.rollback()
            return False

    @log
    def supprimer_like(self, id_user, id_activite) -> bool:
        """Suppression d'un like dans la base de données.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur qui a aimé l'activité.
        id_activite : int
            Identifiant de l'activité aimée.

        Returns
        -------
        bool
            True si le like a été supprimé avec succès, False en cas d'erreur ou si le like n'existe pas.
        """
        try:
            like_to_delete = (
                self.session.query(Like).filter_by(id_user=id_user, id_activite=id_activite).first()
            )
            if like_to_delete:
                self.session.delete(like_to_delete)
                self.session.commit()
                return True
            return False
        except Exception as e:
            logging.info(e)
            self.session.rollback()
            return False

    @log
    def get_likes_by_activity(self, id_activite) -> list[Like]:
        """Récupère tous les likes associés à une activité.

        Parameters
        ----------
        id_activite : int
            Identifiant de l'activité pour laquelle on récupère les likes.

        Returns
        -------
        list[Like]
            Liste des objets `Like` associés à l'activité. Retourne une liste vide en cas d'erreur.
        """
        try:
            likes = self.session.query(Like).filter_by(id_activite=id_activite).all()
            return likes
        except Exception as e:
            logging.info(e)
            return []

    @log
    def count_likes_by_activity(self, id_activite) -> int:
        """Compte le nombre de likes d'une activité.

        Parameters
        ----------
        id_activite : int
            Identifiant de l'activité pour laquelle on compte les likes.

        Returns
        -------
        int
            Nombre de likes associés à l'activité. Retourne 0 en cas d'erreur.
        """
        try:
            count = self.session.query(Like).filter_by(id_activite=id_activite).count()
            return count
        except Exception as e:
            logging.info(e)
            return 0

    @log
    def user_a_like(self, id_user, id_activite) -> bool:
        """Vérifie si un utilisateur a déjà liké une activité.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur.
        id_activite : int
            Identifiant de l'activité.

        Returns
        -------
        bool
            True si l'utilisateur a déjà liké l'activité, False sinon ou en cas d'erreur.
        """
        try:
            like_exists = (
                self.session.query(Like).filter_by(id_user=id_user, id_activite=id_activite).first()
            )
            return like_exists is not None
        except Exception as e:
            logging.info(e)
            return False

    @log
    def get_likes_by_user(self, id_user) -> list[Like]:
        """Récupère tous les likes d'un utilisateur.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur pour lequel on récupère les likes.

        Returns
        -------
        list[Like]
            Liste des objets `Like` associés à l'utilisateur. Retourne une liste vide en cas d'erreur.
        """
        try:
            likes = self.session.query(Like).filter_by(id_user=id_user).all()
            return likes
        except Exception as e:
            logging.info(e)
            return []
