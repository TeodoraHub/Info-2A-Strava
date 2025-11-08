import logging
from typing import List, Optional

from business_object.user_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class UtilisateurDAO(metaclass=Singleton):
    """Accès aux utilisateurs stockés en base via psycopg2."""

    @log
    def creer(self, utilisateur: Utilisateur) -> bool:
        """Insère un utilisateur et alimente son identifiant."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO utilisateur (nom_user, mail_user, mdp)
                        VALUES (%s, %s, %s)
                        RETURNING id_user
                        """,
                        (utilisateur.nom_user, utilisateur.mail_user, utilisateur.mdp),
                    )
                    row = cursor.fetchone()
                    if row and row.get("id_user") is not None:
                        utilisateur.id_user = row["id_user"]
                        connection.commit()
                        return True
                    connection.rollback()
                    return False
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la création de l'utilisateur : %s", exc)
            return False

    @log
    def trouver_par_id(self, id_user: int) -> Optional[Utilisateur]:
        """Retourne un utilisateur par son identifiant."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_user, nom_user, mail_user, mdp
                        FROM utilisateur
                        WHERE id_user = %s
                        """,
                        (id_user,),
                    )
                    row = cursor.fetchone()
                    if row:
                        return Utilisateur(
                            id_user=row.get("id_user"),
                            nom_user=row.get("nom_user"),
                            mail_user=row.get("mail_user"),
                            mdp=row.get("mdp"),
                        )
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la recherche de l'utilisateur : %s", exc)
        return None

    @log
    def lister_tous(self) -> List[Utilisateur]:
        """Liste l'ensemble des utilisateurs."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_user, nom_user, mail_user, mdp FROM utilisateur"
                    )
                    rows = cursor.fetchall() or []
                    return [
                        Utilisateur(
                            id_user=row.get("id_user"),
                            nom_user=row.get("nom_user"),
                            mail_user=row.get("mail_user"),
                            mdp=row.get("mdp"),
                        )
                        for row in rows
                    ]
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la récupération des utilisateurs : %s", exc)
        return []

    @log
    def modifier(self, utilisateur: Utilisateur) -> bool:
        """Met à jour un utilisateur existant."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateur
                        SET nom_user = %s, mail_user = %s, mdp = %s
                        WHERE id_user = %s
                        """,
                        (
                            utilisateur.nom_user,
                            utilisateur.mail_user,
                            utilisateur.mdp,
                            utilisateur.id_user,
                        ),
                    )
                    if getattr(cursor, "rowcount", 0) > 0:
                        connection.commit()
                        return True
                    connection.rollback()
                    return False
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la modification de l'utilisateur : %s", exc)
            return False

    @log
    def supprimer(self, utilisateur: Utilisateur) -> bool:
        """Supprime un utilisateur."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utilisateur WHERE id_user = %s",
                        (utilisateur.id_user,),
                    )
                    if getattr(cursor, "rowcount", 0) > 0:
                        connection.commit()
                        return True
                    connection.rollback()
                    return False
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la suppression de l'utilisateur : %s", exc)
            return False

    @log
    def se_connecter(self, nom_user: str, mdp: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur via son nom et mot de passe."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_user, nom_user, mail_user, mdp
                        FROM utilisateur
                        WHERE nom_user = %s AND mdp = %s
                        """,
                        (nom_user, mdp),
                    )
                    row = cursor.fetchone()
                    if row:
                        return Utilisateur(
                            id_user=row.get("id_user"),
                            nom_user=row.get("nom_user"),
                            mail_user=row.get("mail_user"),
                            mdp=row.get("mdp"),
                        )
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la connexion de l'utilisateur : %s", exc)
        return None
