import logging
from datetime import datetime

from business_object.like_comment_object.like import Like
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class LikeDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Likes de la base de données via SQLAlchemy"""

    def __init__(self):
        self.session = DBConnection().session  # Récupère la session SQLAlchemy depuis DBConnection

    @log
    def creer_like(self, id_user, id_activite) -> bool:
        """Création d'un like dans la base de données"""
        try:
            new_like = Like(id_user=id_user, id_activite=id_activite, date_like=datetime.now())
            self.session.add(new_like)
            self.session.commit()
            return True
        except Exception as e:
            logging.info(e)
            self.session.rollback()
            return False

    @log
    def supprimer_like(self, id_user, id_activite) -> bool:
        """Suppression d'un like dans la base de données"""
        try:
            like_to_delete = (
                self.session.query(Like).filter_by(id_user=id_user, id_activite=id_activite).first()
            )
            if like_to_delete:
                self.session.delete(like_to_delete)
                self.session.commit()
                return True
            return False
        except Exception as e:
            logging.info(e)
            self.session.rollback()
            return False

    @log
    def get_likes_by_activity(self, id_activite) -> list[Like]:
        """Récupère tous les likes d'une activité"""
        try:
            likes = self.session.query(Like).filter_by(id_activite=id_activite).all()
            return likes
        except Exception as e:
            logging.info(e)
            return []

    @log
    def count_likes_by_activity(self, id_activite) -> int:
        """Compte le nombre de likes d'une activité"""
        try:
            count = self.session.query(Like).filter_by(id_activite=id_activite).count()
            return count
        except Exception as e:
            logging.info(e)
            return 0

    @log
    def user_a_like(self, id_user, id_activite) -> bool:
        """Vérifie si un utilisateur a déjà liké une activité"""
        try:
            like_exists = (
                self.session.query(Like).filter_by(id_user=id_user, id_activite=id_activite).first()
            )
            return like_exists is not None
        except Exception as e:
            logging.info(e)
            return False

    @log
    def get_likes_by_user(self, id_user) -> list[Like]:
        """Récupère tous les likes d'un utilisateur"""
        try:
            likes = self.session.query(Like).filter_by(id_user=id_user).all()
            return likes
        except Exception as e:
            logging.info(e)
            return []
            logging.info(e)
            return []
