import logging

from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class SuiviDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux relations de suivi dans la base de données"""

    @log
    def creer_suivi(self, id_suiveur, id_suivi) -> bool:
        """Création d'une relation de suivi dans la base de données

        Parameters
        ----------
        id_suiveur : int
            identifiant de l'utilisateur qui suit
        id_suivi : int
            identifiant de l'utilisateur suivi

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        # Vérifier qu'un utilisateur ne se suit pas lui-même
        if id_suiveur == id_suivi:
            logging.info("Un utilisateur ne peut pas se suivre lui-même")
            return False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO suivi(id_suiveur, id_suivi) VALUES        "
                        "(%(id_suiveur)s, %(id_suivi)s);                       ",
                        {
                            "id_suiveur": id_suiveur,
                            "id_suivi": id_suivi,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            return False

        return res > 0

    @log
    def supprimer_suivi(self, id_suiveur, id_suivi) -> bool:
        """Suppression d'une relation de suivi dans la base de données

        Parameters
        ----------
        id_suiveur : int
            identifiant de l'utilisateur qui suit
        id_suivi : int
            identifiant de l'utilisateur suivi

        Returns
        -------
        deleted : bool
            True si la suppression est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM suivi                       "
                        " WHERE id_suiveur=%(id_suiveur)s        "
                        "   AND id_suivi=%(id_suivi)s;           ",
                        {"id_suiveur": id_suiveur, "id_suivi": id_suivi},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            return False

        return res > 0

    @log
    def get_followers(self, id_user) -> list[int]:
        """Récupère la liste des followers d'un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        followers : list[int]
            liste des id des utilisateurs qui suivent cet utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_suiveur                        "
                        "  FROM suivi                             "
                        " WHERE id_suivi = %(id_user)s;           ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        followers = []
        if res:
            followers = [row["id_suiveur"] for row in res]

        return followers

    @log
    def get_following(self, id_user) -> list[int]:
        """Récupère la liste des utilisateurs suivis par un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        following : list[int]
            liste des id des utilisateurs suivis par cet utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_suivi                          "
                        "  FROM suivi                             "
                        " WHERE id_suiveur = %(id_user)s;         ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        following = []
        if res:
            following = [row["id_suivi"] for row in res]

        return following

    @log
    def user_suit(self, id_suiveur, id_suivi) -> bool:
        """Vérifie si un utilisateur en suit un autre

        Parameters
        ----------
        id_suiveur : int
            identifiant de l'utilisateur qui suit
        id_suivi : int
            identifiant de l'utilisateur potentiellement suivi

        Returns
        -------
        suit : bool
            True si id_suiveur suit id_suivi
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb                    "
                        "  FROM suivi                             "
                        " WHERE id_suiveur = %(id_suiveur)s       "
                        "   AND id_suivi = %(id_suivi)s;          ",
                        {"id_suiveur": id_suiveur, "id_suivi": id_suivi},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return False

        return res["nb"] > 0 if res else False

    @log
    def count_followers(self, id_user) -> int:
        """Compte le nombre de followers d'un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        count : int
            nombre de followers
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb_followers          "
                        "  FROM suivi                             "
                        " WHERE id_suivi = %(id_user)s;           ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return 0

        return res["nb_followers"] if res else 0

    @log
    def count_following(self, id_user) -> int:
        """Compte le nombre d'utilisateurs suivis par un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        count : int
            nombre d'utilisateurs suivis
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb_following          "
                        "  FROM suivi                             "
                        " WHERE id_suiveur = %(id_user)s;         ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return 0

        return res["nb_following"] if res else 0
