import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from business_object.suivi import Suivi
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class SuiviDAO(metaclass=Singleton):
    """Acces aux relations de suivi."""

    def __init__(self, session_factory: sessionmaker | None = None):
        self._session_factory = session_factory or DBConnection().session_factory

    @log
    def creer_suivi(self, id_suiveur: int, id_suivi: int) -> bool:
        if id_suiveur == id_suivi:
            logging.info("Un utilisateur ne peut pas se suivre lui-meme")
            return False

        with self._session_factory() as session:
            try:
                suivi = Suivi(id_suiveur=id_suiveur, id_suivi=id_suivi)
                session.add(suivi)
                session.commit()
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                logging.error(f"Erreur lors de la creation du suivi : {exc}")
                return False

    @log
    def supprimer_suivi(self, id_suiveur: int, id_suivi: int) -> bool:
        with self._session_factory() as session:
            try:
                suivi = session.query(Suivi).filter_by(id_suiveur=id_suiveur, id_suivi=id_suivi).first()
                if not suivi:
                    logging.info("La relation de suivi n'existe pas.")
                    return False
                session.delete(suivi)
                session.commit()
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                logging.error(f"Erreur lors de la suppression du suivi : {exc}")
                return False

    @log
    def get_followers(self, id_user: int) -> list[int]:
        with self._session_factory() as session:
            try:
                followers = (
                    session.query(Suivi.id_suiveur)
                    .filter(Suivi.id_suivi == id_user)
                    .all()
                )
                return [f[0] for f in followers]
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la recuperation des followers : {exc}")
                return []

    @log
    def get_following(self, id_user: int) -> list[int]:
        with self._session_factory() as session:
            try:
                following = (
                    session.query(Suivi.id_suivi)
                    .filter(Suivi.id_suiveur == id_user)
                    .all()
                )
                return [f[0] for f in following]
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la recuperation des utilisateurs suivis : {exc}")
                return []

    @log
    def user_suit(self, id_suiveur: int, id_suivi: int) -> bool:
        with self._session_factory() as session:
            try:
                suit = session.query(Suivi).filter_by(id_suiveur=id_suiveur, id_suivi=id_suivi).first()
                return suit is not None
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la verification du suivi : {exc}")
                return False

    @log
    def count_followers(self, id_user: int) -> int:
        with self._session_factory() as session:
            try:
                return session.query(Suivi).filter(Suivi.id_suivi == id_user).count()
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors du comptage des followers : {exc}")
                return 0

    @log
    def count_following(self, id_user: int) -> int:
        with self._session_factory() as session:
            try:
                return session.query(Suivi).filter(Suivi.id_suiveur == id_user).count()
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors du comptage des suivis : {exc}")
                return 0
