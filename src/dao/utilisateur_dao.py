import logging

from business_object.User_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class UtilisateurDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Utilisateurs de la base de données"""

    @log
    def creer(self, utilisateur) -> bool:
        """Creation d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

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
                        "INSERT INTO utilisateur(nom_user, mail_user, mdp) VALUES        "
                        "(%(nom_user)s, %(mail_user)s, %(mdp)s)             "
                        "  RETURNING id_user;           ",
                        {
                            "nom_user": utilisateur.nom_user,
                            "mail_user": utilisateur.mail_user,
                            "mdp": utilisateur.mdp,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            utilisateur.id_user = res["id_user"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_user) -> Utilisateur:
        """trouver un utilisateur grace à son id

        Parameters
        ----------
        id_user : int
            numéro id de l'utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE id_user = %(id_user)s;  ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                nom_user=res["nom_user"],
                mail_user=res["mail_user"],
                mdp=res["mdp"],
                id_user=res["id_user"],
            )

        return utilisateur

    @log
    def lister_tous(self) -> list[Utilisateur]:
        """lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateur]
            renvoie la liste de tous les utilisateurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM utilisateur;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_utilisateurs = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id_user=row["id_user"],
                    nom_user=row["nom_user"],
                    mdp=row["mdp"],
                    mail_user=row["mail_user"],
                )

                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    @log
    def modifier(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE utilisateur                                      "
                        "   SET nom_user      = %(nom_user)s,                   "
                        "       mail_user         = %(mail_user)s,                      "
                        "       mdp = %(mdp)s               "
                        " WHERE id_user = %(id_user)s;                  ",
                        {
                            "nom_user": utilisateur.nom_user,
                            "mail_user": utilisateur.mail_user,
                            "mdp": utilisateur.mdp,
                            "id_user": utilisateur.id_user,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            utilisateur à supprimer de la base de données

        Returns
        -------
            True si le utilisateur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un utilisateur
                    cursor.execute(
                        "DELETE FROM utilisateur                   WHERE id_user=%(id_user)s      ",
                        {"id_user": utilisateur.id_user},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, nom_user, mdp) -> Utilisateur:
        """se connecter grâce à son nom_user et son mot de passe

        Parameters
        ----------
        nom_user : str
            nom_user du utilisateur que l'on souhaite trouver
        mdp : str
            mot de passe du utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            renvoie le utilisateur que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE nom_user = %(nom_user)s         "
                        "   AND mdp = %(mdp)s;              ",
                        {"nom_user": nom_user, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        utilisateur = None

        if res:
            utilisateur = Utilisateur(
                nom_user=res["nom_user"],
                mdp=res["mdp"],
                mail_user=res["mail_user"],
                id_user=res["id_user"],
            )

        return utilisateur
