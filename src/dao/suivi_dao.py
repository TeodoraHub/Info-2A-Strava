import logging
from typing import List

from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class SuiviDAO(metaclass=Singleton):
    """Accès aux relations de suivi en base via psycopg2."""

    @staticmethod
    def _extract_scalar(row, key: str, default: int = 0) -> int:
        return row.get(key, default) if row else default

    @staticmethod
    def _extract_list(rows, key: str) -> List[int]:
        if not rows:
            return []
        return [row.get(key) for row in rows if row and row.get(key) is not None]

    @log
    def creer_suivi(self, id_suiveur: int, id_suivi: int) -> bool:
        """Crée une relation de suivi."""

        if id_suiveur == id_suivi:
            logging.info("Un utilisateur ne peut pas se suivre lui-même")
            return False

        connection = None
        try:
            connection_manager = DBConnection().connection
            with connection_manager as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO suivi (id_suiveur, id_suivi)
                        VALUES (%s, %s)
                        """,
                        (id_suiveur, id_suivi),
                    )
                    if getattr(cursor, "rowcount", 0) > 0:
                        connection.commit()
                        return True
                    connection.rollback()
                    return False
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la création du suivi : %s", exc)
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:  # pragma: no cover - best effort
                    pass
            return False

    @log
    def supprimer_suivi(self, id_suiveur: int, id_suivi: int) -> bool:
        """Supprime une relation de suivi."""

        connection = None
        try:
            connection_manager = DBConnection().connection
            with connection_manager as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM suivi WHERE id_suiveur = %s AND id_suivi = %s",
                        (id_suiveur, id_suivi),
                    )
                    if getattr(cursor, "rowcount", 0) > 0:
                        connection.commit()
                        return True
                    connection.rollback()
                    return False
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la suppression du suivi : %s", exc)
            if connection is not None:
                try:
                    connection.rollback()
                except Exception:  # pragma: no cover
                    pass
            return False

    @log
    def get_followers(self, id_user: int) -> List[int]:
        """Retourne la liste des followers d'un utilisateur."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_suiveur FROM suivi WHERE id_suivi = %s",
                        (id_user,),
                    )
                    rows = cursor.fetchall()
                    return self._extract_list(rows, "id_suiveur")
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error(
                "Erreur lors de la récupération des followers pour l'utilisateur %s : %s",
                id_user,
                exc,
            )
            return []

    @log
    def get_following(self, id_user: int) -> List[int]:
        """Retourne la liste des utilisateurs suivis."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_suivi FROM suivi WHERE id_suiveur = %s",
                        (id_user,),
                    )
                    rows = cursor.fetchall()
                    return self._extract_list(rows, "id_suivi")
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error(
                "Erreur lors de la récupération des suivis pour l'utilisateur %s : %s",
                id_user,
                exc,
            )
            return []

    @log
    def user_suit(self, id_suiveur: int, id_suivi: int) -> bool:
        """Indique si un utilisateur en suit un autre."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) AS nb
                        FROM suivi
                        WHERE id_suiveur = %s AND id_suivi = %s
                        """,
                        (id_suiveur, id_suivi),
                    )
                    row = cursor.fetchone()
                    return self._extract_scalar(row, "nb") > 0
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error("Erreur lors de la vérification du suivi : %s", exc)
            return False

    @log
    def count_followers(self, id_user: int) -> int:
        """Compte le nombre de followers."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) AS nb_followers
                        FROM suivi
                        WHERE id_suivi = %s
                        """,
                        (id_user,),
                    )
                    row = cursor.fetchone()
                    return self._extract_scalar(row, "nb_followers")
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error(
                "Erreur lors du comptage des followers pour l'utilisateur %s : %s",
                id_user,
                exc,
            )
            return 0

    @log
    def count_following(self, id_user: int) -> int:
        """Compte le nombre d'utilisateurs suivis."""

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) AS nb_following
                        FROM suivi
                        WHERE id_suiveur = %s
                        """,
                        (id_user,),
                    )
                    row = cursor.fetchone()
                    return self._extract_scalar(row, "nb_following")
        except Exception as exc:  # pragma: no cover - log + retour contrôlé
            logging.error(
                "Erreur lors du comptage des suivis pour l'utilisateur %s : %s",
                id_user,
                exc,
            )
            return 0
