import logging
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from business_object.user_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class UtilisateurDAO(metaclass=Singleton):
    """Operations CRUD sur la table utilisateur."""

    def __init__(self, session_factory: sessionmaker | None = None):
        self._session_factory = session_factory or DBConnection().session_factory

    @log
    def creer(self, utilisateur: Utilisateur) -> bool:
        with self._session_factory() as session:
            try:
                session.add(utilisateur)
                session.commit()
                session.refresh(utilisateur)
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                logging.error(f"Erreur lors de la creation de l'utilisateur : {exc}")
                return False

    @log
    def trouver_par_id(self, id_user: int) -> Optional[Utilisateur]:
        with self._session_factory() as session:
            try:
                return session.get(Utilisateur, id_user)
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la recherche de l'utilisateur : {exc}")
                return None

    @log
    def lister_tous(self) -> List[Utilisateur]:
        with self._session_factory() as session:
            try:
                return session.query(Utilisateur).all()
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la recuperation des utilisateurs : {exc}")
                return []

    @log
    def modifier(self, utilisateur: Utilisateur) -> bool:
        with self._session_factory() as session:
            try:
                existing_user = session.get(Utilisateur, utilisateur.id_user)
                if not existing_user:
                    return False
                existing_user.nom_user = utilisateur.nom_user
                existing_user.mail_user = utilisateur.mail_user
                existing_user.mdp = utilisateur.mdp
                session.commit()
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                logging.error(f"Erreur lors de la modification de l'utilisateur : {exc}")
                return False

    @log
    def supprimer(self, utilisateur: Utilisateur) -> bool:
        with self._session_factory() as session:
            try:
                existing_user = session.get(Utilisateur, utilisateur.id_user)
                if not existing_user:
                    return False
                session.delete(existing_user)
                session.commit()
                return True
            except SQLAlchemyError as exc:
                session.rollback()
                logging.error(f"Erreur lors de la suppression de l'utilisateur : {exc}")
                return False

    @log
    def se_connecter(self, nom_user: str, mdp: str) -> Optional[Utilisateur]:
        with self._session_factory() as session:
            try:
                utilisateur = session.query(Utilisateur).filter_by(nom_user=nom_user, mdp=mdp).first()
                if utilisateur:
                    session.expunge(utilisateur)
                return utilisateur
            except SQLAlchemyError as exc:
                logging.error(f"Erreur lors de la connexion de l'utilisateur : {exc}")
                return None
