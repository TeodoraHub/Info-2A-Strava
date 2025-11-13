import logging
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from business_object.like_comment_object.commentaire import Commentaire
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class CommentaireDAO(metaclass=Singleton):
    """Acces aux commentaires via SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker | None = None):
        self._session_factory = session_factory or DBConnection().session_factory

    @log
    def creer_commentaire(self, id_user: int, id_activite: int, contenu: str) -> Commentaire | None:
        """Cree et persiste un commentaire."""
        with self._session_factory() as session:
            try:
                commentaire = Commentaire(
                    id_user=id_user,
                    id_activite=id_activite,
                    contenu=contenu,
                    date_comment=datetime.now(),
                )
                session.add(commentaire)
                session.commit()
                session.refresh(commentaire)
                return commentaire
            except Exception as exc:
                session.rollback()
                logging.error(f"Erreur lors de la crNation du commentaire: {exc}")
                return None

    @log
    def supprimer_commentaire(self, id_comment: int) -> bool:
        """Supprime un commentaire par identifiant."""
        with self._session_factory() as session:
            try:
                commentaire = session.get(Commentaire, id_comment)
                if not commentaire:
                    return False
                session.delete(commentaire)
                session.commit()
                return True
            except Exception as exc:
                session.rollback()
                logging.error(f"Erreur lors de la suppression du commentaire: {exc}")
                return False

    @log
    def get_commentaires_by_activity(self, id_activite: int) -> list[Commentaire]:
        """Retourne les commentaires d'une activite."""
        with self._session_factory() as session:
            try:
                return (
                    session.query(Commentaire)
                    .filter_by(id_activite=id_activite)
                    .order_by(Commentaire.date_comment.desc())
                    .all()
                )
            except Exception as exc:
                logging.error(f"Erreur lors de la rNcupNration des commentaires: {exc}")
                return []

    @log
    def get_commentaires_by_user(self, id_user: int) -> list[Commentaire]:
        """Retourne les commentaires crees par un utilisateur."""
        with self._session_factory() as session:
            try:
                return (
                    session.query(Commentaire)
                    .filter_by(id_user=id_user)
                    .order_by(Commentaire.date_comment.desc())
                    .all()
                )
            except Exception as exc:
                logging.error(f"Erreur lors de la rNcupNration des commentaires: {exc}")
                return []

    @log
    def count_commentaires_by_activity(self, id_activite: int) -> int:
        """Compte le nombre de commentaires d'une activite."""
        with self._session_factory() as session:
            try:
                return session.query(Commentaire).filter_by(id_activite=id_activite).count()
            except Exception as exc:
                logging.error(f"Erreur lors du comptage des commentaires: {exc}")
                return 0

    @log
    def modifier_commentaire(self, id_comment: int, nouveau_contenu: str) -> bool:
        """Met a jour le contenu d'un commentaire existant."""
        with self._session_factory() as session:
            try:
                commentaire = session.get(Commentaire, id_comment)
                if not commentaire:
                    return False
                commentaire.contenu = nouveau_contenu
                session.commit()
                return True
            except Exception as exc:
                session.rollback()
                logging.error(f"Erreur lors de la modification du commentaire: {exc}")
                return False
