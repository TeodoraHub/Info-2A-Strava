import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from business_object.like_comment_object.like import Like
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class LikeDAO(metaclass=Singleton):
    """Acces aux likes via SQLAlchemy."""

    def __init__(self, session_factory: sessionmaker | None = None):
        self._session_factory = session_factory or DBConnection().session_factory

    @log
    def creer_like(self, id_user: int, id_activite: int) -> bool:
        """Cree un like si l'utilisateur ne l'a pas deja enregistre."""
        with self._session_factory() as session:
            try:
                like = Like(id_user=id_user, id_activite=id_activite, date_like=datetime.utcnow())
                session.add(like)
                session.commit()
                return True
            except IntegrityError:
                session.rollback()
                logging.info("Like deja existant pour user=%s activite=%s", id_user, id_activite)
                return False
            except Exception as exc:
                session.rollback()
                logging.error(f"Echec de l'insertion de like: {exc}")
                return False

    @log
    def supprimer_like(self, id_user: int, id_activite: int) -> bool:
        """Supprime un like user/activite."""
        with self._session_factory() as session:
            try:
                like_to_delete = (
                    session.query(Like).filter_by(id_user=id_user, id_activite=id_activite).first()
                )
                if not like_to_delete:
                    return False
                session.delete(like_to_delete)
                session.commit()
                return True
            except Exception as exc:
                session.rollback()
                logging.error(exc)
                return False

    @log
    def get_likes_by_activity(self, id_activite: int) -> list[Like]:
        """Liste tous les likes associes a une activite."""
        with self._session_factory() as session:
            try:
                return session.query(Like).filter_by(id_activite=id_activite).all()
            except Exception as exc:
                logging.error(exc)
                return []

    @log
    def count_likes_by_activity(self, id_activite: int) -> int:
        """Compte les likes d'une activite."""
        with self._session_factory() as session:
            try:
                return session.query(Like).filter_by(id_activite=id_activite).count()
            except Exception as exc:
                logging.error(exc)
                return 0

    @log
    def user_a_like(self, id_user: int, id_activite: int) -> bool:
        """Indique si l'utilisateur a deja like l'activite."""
        with self._session_factory() as session:
            try:
                like_exists = (
                    session.query(Like.id_like)
                    .filter_by(id_user=id_user, id_activite=id_activite)
                    .first()
                )
                return like_exists is not None
            except Exception as exc:
                logging.error(exc)
                return False

    @log
    def get_likes_by_user(self, id_user: int) -> list[Like]:
        """Retourne les likes d'un utilisateur."""
        with self._session_factory() as session:
            try:
                return session.query(Like).filter_by(id_user=id_user).all()
            except Exception as exc:
                logging.error(exc)
                return []
