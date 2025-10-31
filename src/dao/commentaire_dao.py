import logging

from business_object.like_comment_object.commentaire import Commentaire
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class CommentaireDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""

    @log
    def creer_commentaire(self, id_user, id_activite, contenu) -> bool:
        """Creation d'un commentaire dans la base de données

        Parameters
        ----------
        id_user : int
        id_activite : int
        contenu : str

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
                        "INSERT INTO commentaire(id_user, id, contenu) VALUES        "
                        "(%(id_user)s, %(id_activite)s, %(contenu)s)             "
                        "  RETURNING id_comment;                                                ",
                        {
                            "id_user": id_user,
                            "id_activite": id_activite,
                            "contenu": contenu,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            created = True

        return created

    @log
    def supprimer_commentaire(self, id_comment) -> bool:
        """Suppression d'un commentaire dans la base de données

        Parameters
        ----------
        id_comment : int
            identifiant du commentaire

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
                        "DELETE FROM commentaire                  "
                        " WHERE id_comment=%(id_comment)s;        ",
                        {"id_comment": id_comment},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            return False

        return res > 0

    @log
    def get_commentaires_by_activity(self, id_activite) -> list[Commentaire]:
        """Récupère tous les commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        liste_commentaires : list[Commentaire]
            liste des commentaires de l'activité
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM commentaire                    "
                        " WHERE id = %(id_activite)s           "
                        " ORDER BY date_comment DESC;          ",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        liste_commentaires = []
        if res:
            for row in res:
                commentaire = Commentaire(
                    id_comment=row["id_comment"],
                    id_user=row["id_user"],
                    id_activite=row["id"],
                    contenu=row["contenu"],
                    date_comment=row["date_comment"],
                )
                liste_commentaires.append(commentaire)

        return liste_commentaires

    @log
    def get_commentaires_by_user(self, id_user) -> list[Commentaire]:
        """Récupère tous les commentaires d'un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        liste_commentaires : list[Commentaire]
            liste des commentaires de l'utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM commentaire                    "
                        " WHERE id_user = %(id_user)s          "
                        " ORDER BY date_comment DESC;          ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            return []

        liste_commentaires = []
        if res:
            for row in res:
                commentaire = Commentaire(
                    id_comment=row["id_comment"],
                    id_user=row["id_user"],
                    id_activite=row["id"],
                    contenu=row["contenu"],
                    date_comment=row["date_comment"],
                )
                liste_commentaires.append(commentaire)

        return liste_commentaires

    @log
    def count_commentaires_by_activity(self, id_activite) -> int:
        """Compte le nombre de commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        count : int
            nombre de commentaires de l'activité
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as nb_comments        "
                        "  FROM commentaire                    "
                        " WHERE id = %(id_activite)s;          ",
                        {"id_activite": id_activite},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return 0

        return res["nb_comments"] if res else 0

    @log
    def modifier_commentaire(self, id_comment, nouveau_contenu) -> bool:
        """Modification d'un commentaire dans la base de données

        Parameters
        ----------
        id_comment : int
            identifiant du commentaire
        nouveau_contenu : str
            nouveau contenu du commentaire

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE commentaire                    "
                        "   SET contenu = %(contenu)s          "
                        " WHERE id_comment = %(id_comment)s;   ",
                        {"contenu": nouveau_contenu, "id_comment": id_comment},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            return False

        return res == 1
