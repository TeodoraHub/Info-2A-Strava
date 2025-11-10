import logging
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from business_object.like_comment_object.commentaire import Commentaire
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class CommentaireDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""

    def __init__(self):
        """Initialise la classe avec la connexion à la base de données."""
        self.Session = sessionmaker(bind=DBConnection().engine)

    @log
    def creer_commentaire(self, id_utilisateur: int, id_activite: int, contenu: str) -> Commentaire:
        """Création d'un commentaire dans la base de données.

        Parameters
        ----------
        id_utilisateur : int
            Identifiant de l'utilisateur qui crée le commentaire.
        id_activite : int
            Identifiant de l'activité associée au commentaire.
        contenu : str
            Contenu du commentaire.

        Returns
        -------
        Commentaire
            L'instance du commentaire créé, ou None en cas d'erreur.
        """
        session = self.Session()
        try:
            commentaire = Commentaire(
                id_utilisateur=id_utilisateur,
                id_activite=id_activite,
                contenu=contenu,
                date_commentaire=datetime.now(),
            )
            session.add(commentaire)
            session.commit()  # Validation de la transaction
            return commentaire
        except Exception as e:
            session.rollback()  # Annuler en cas d'erreur
            logging.error(f"Erreur lors de la création du commentaire: {e}")
            return None
        finally:
            session.close()

    @log
    def supprimer_commentaire(self, id_comment: int) -> bool:
        """Suppression d'un commentaire dans la base de données.

        Parameters
        ----------
        id_comment : int
            Identifiant du commentaire à supprimer.

        Returns
        -------
        bool
            True si la suppression est réussie, False sinon.
        """
        session = self.Session()
        try:
            commentaire = session.query(Commentaire).filter_by(id_comment=id_comment).first()
            if commentaire:
                session.delete(commentaire)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la suppression du commentaire: {e}")
            return False
        finally:
            session.close()

    @log
    def get_commentaires_by_activity(self, id_activite: int) -> list[Commentaire]:
        """Récupère tous les commentaires d'une activité.

        Parameters
        ----------
        id_activite : int
            Identifiant de l'activité pour laquelle on récupère les commentaires.

        Returns
        -------
        list[Commentaire]
            Liste des commentaires associés à l'activité, triés par date décroissante.
        """
        session = self.Session()
        try:
            commentaires = (
                session.query(Commentaire)
                .filter_by(id_activite=id_activite)
                .order_by(Commentaire.date_commentaire.desc())
                .all()
            )
            return commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []
        finally:
            session.close()

    @log
    def get_commentaires_by_user(self, id_user: int) -> list[Commentaire]:
        """Récupère tous les commentaires d'un utilisateur.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur pour lequel on récupère les commentaires.

        Returns
        -------
        list[Commentaire]
            Liste des commentaires créés par l'utilisateur, triés par date décroissante.
        """
        session = self.Session()
        try:
            commentaires = (
                session.query(Commentaire)
                .filter_by(id_user=id_user)
                .order_by(Commentaire.date_commentaire.desc())
                .all()
            )
            return commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []
        finally:
            session.close()

    @log
    def count_commentaires_by_activity(self, id_activite: int) -> int:
        """Compte le nombre de commentaires d'une activité.

        Parameters
        ----------
        id_activite : int
            Identifiant de l'activité pour laquelle on compte les commentaires.

        Returns
        -------
        int
            Nombre de commentaires associés à l'activité.
        """
        session = self.Session()
        try:
            count = session.query(Commentaire).filter_by(id_activite=id_activite).count()
            return count
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires: {e}")
            return 0
        finally:
            session.close()

    @log
    def modifier_commentaire(self, id_comment: int, nouveau_contenu: str) -> bool:
        """Modification d'un commentaire dans la base de données.

        Parameters
        ----------
        id_comment : int
            Identifiant du commentaire à modifier.
        nouveau_contenu : str
            Nouveau contenu du commentaire.

        Returns
        -------
        bool
            True si la modification est réussie, False sinon.
        """
        session = self.Session()
        try:
            commentaire = session.query(Commentaire).filter_by(id_comment=id_comment).first()
            if commentaire:
                commentaire.contenu = nouveau_contenu
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logging.error(f"Erreur lors de la modification du commentaire: {e}")
            return False
        finally:
            session.close()
