import logging

from business_object.like_comment_object.like import Like
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class LikeDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Likes de la base de données"""

    @log
    def creer_like(self, id_user, id_activite) -> bool:
        """Création d'un like dans la base de données

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur qui like
        id_activite : int
            identifiant de l'activité likée

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO liker(id_user, id) VALUES        "
                        "(%(id_user)s, %(id_activite)s)             "
                        "  RETURNING id_like;                                                ",
                        {
                            "id_user": id_user,
                            "id_activite": id_activite,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return False

        return res is not None

    @log
    def supprimer_like(self, id_user, id_activite) -> bool:
        """Suppression d'un like dans la base de données

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur
        id_activite : int
            identifiant de l'activité

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
                        "DELETE FROM liker                  "
                        " WHERE id_user=%(id_user)s      "
                        "   AND id=%(id_activite)s;      ",
                        {"id_user": id_user, "id_activite": id_activite},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            return False

        return res > 0

    @log
    def get_likes_by_activity(self, id_activite) -> list[Like]:
        """Récupère tous les likes d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        liste_likes : list[Like]
            liste des likes de l'activité
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM liker                          "
                        " WHERE id = %(id_activite)s;          ",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        liste_likes = []
        if res:
            for row in res:
                like = Like(
                    id_activite=row["id"], id_user=row["id_user"], date_like=row["date_like"]
                )
                liste_likes.append(like)

        return liste_likes

    @log
    def count_likes_by_activity(self, id_activite) -> int:
        """Compte le nombre de likes d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        count : int
            nombre de likes de l'activité
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb_likes           "
                        "  FROM liker                          "
                        " WHERE id = %(id_activite)s;          ",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return 0

        return res["nb_likes"] if res else 0

    @log
    def user_a_like(self, id_user, id_activite) -> bool:
        """Vérifie si un utilisateur a déjà liké une activité

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        has_liked : bool
            True si l'utilisateur a déjà liké
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb                 "
                        "  FROM liker                          "
                        " WHERE id_user = %(id_user)s          "
                        "   AND id = %(id_activite)s;          ",
                        {"id_user": id_user, "id_activite": id_activite},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return False

        return res["nb"] > 0 if res else False

    @log
    def get_likes_by_user(self, id_user) -> list[Like]:
        """Récupère tous les likes d'un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        liste_likes : list[Like]
            liste des likes de l'utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM liker                          "
                        " WHERE id_user = %(id_user)s;         ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        liste_likes = []
        if res:
            for row in res:
                like = Like(
                    id_activite=row["id"], id_user=row["id_user"], date_like=row["date_like"]
                )
                liste_likes.append(like)

        return liste_likes
