import logging

from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class CommentaireDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""

    @log
    def creer_commentaire(self, id_user, id_activite, contenu) -> bool:
        """Creation d'un commentaire dans la base de données

        Args:
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
                        "INSERT INTO commentaire(id_user, id_activite, contenu) VALUES        "
                        "(%(id_user)s, %(id_activite)s, %(contenu)s)             "
                        "  RETURNING id_commentaire;                                                ",
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
