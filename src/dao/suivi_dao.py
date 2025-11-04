import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from business_object.suivi import Suivi
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class SuiviDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux relations de suivi dans la base de données"""

    @log
    def creer_suivi(self, id_suiveur, id_suivi) -> bool:
        """Création d'une relation de suivi dans la base de données"""

        # Vérifier qu'un utilisateur ne se suit pas lui-même
        if id_suiveur == id_suivi:
            logging.info("Un utilisateur ne peut pas se suivre lui-même")
            return False

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Créer une instance de la relation Suivi
            suivi = Suivi(id_suiveur=id_suiveur, id_suivi=id_suivi)

            # Ajouter et commit la session
            session.add(suivi)
            session.commit()

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Erreur lors de la création du suivi : {str(e)}")
            return False
        finally:
            session.close()

        return True

    @log
    def supprimer_suivi(self, id_suiveur, id_suivi) -> bool:
        """Suppression d'une relation de suivi dans la base de données"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Trouver la relation Suivi
            suivi = session.query(Suivi).filter_by(id_suiveur=id_suiveur, id_suivi=id_suivi).first()

            if suivi:
                session.delete(suivi)
                session.commit()
                return True
            else:
                logging.info("La relation de suivi n'existe pas.")
                return False

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Erreur lors de la suppression du suivi : {str(e)}")
            return False
        finally:
            session.close()

    @log
    def get_followers(self, id_user) -> list[int]:
        """Récupère la liste des followers d'un utilisateur"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Récupérer les suiveurs de l'utilisateur
            followers = session.query(Suivi.id_suiveur).filter(Suivi.id_suivi == id_user).all()

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des followers : {str(e)}")
            return []
        finally:
            session.close()

        # Retourne la liste des id des suiveurs
        return [follower[0] for follower in followers]

    @log
    def get_following(self, id_user) -> list[int]:
        """Récupère la liste des utilisateurs suivis par un utilisateur"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Récupérer les utilisateurs suivis
            following = session.query(Suivi.id_suivi).filter(Suivi.id_suiveur == id_user).all()

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs suivis : {str(e)}")
            return []
        finally:
            session.close()

        # Retourne la liste des id des utilisateurs suivis
        return [follow[0] for follow in following]

    @log
    def user_suit(self, id_suiveur, id_suivi) -> bool:
        """Vérifie si un utilisateur en suit un autre"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Vérifier si la relation de suivi existe
            suit = session.query(Suivi).filter_by(id_suiveur=id_suiveur, id_suivi=id_suivi).first()

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la vérification du suivi : {str(e)}")
            return False
        finally:
            session.close()

        return bool(suit)

    @log
    def count_followers(self, id_user) -> int:
        """Compte le nombre de followers d'un utilisateur"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Compter le nombre de suiveurs
            count = session.query(Suivi).filter(Suivi.id_suivi == id_user).count()

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors du comptage des followers : {str(e)}")
            return 0
        finally:
            session.close()

        return count

    @log
    def count_following(self, id_user) -> int:
        """Compte le nombre d'utilisateurs suivis par un utilisateur"""

        try:
            Session = sessionmaker(bind=DBConnection().engine)
            session = Session()

            # Compter le nombre d'utilisateurs suivis
            count = session.query(Suivi).filter(Suivi.id_suiveur == id_user).count()

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors du comptage des suivis : {str(e)}")
            return 0
        finally:
            session.close()

        return count

        return count
