import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from business_object.user_object.utilisateur import Utilisateur
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class UtilisateurDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Utilisateurs de la base de données via SQLAlchemy"""

    def __init__(self):
        # Récupération de la session SQLAlchemy via sessionmaker
        self.Session = sessionmaker(bind=DBConnection().engine)

    @log
    def creer(self, utilisateur) -> bool:
        """Création d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        session = self.Session()
        try:
            session.add(utilisateur)  # Ajoute l'utilisateur à la session
            session.commit()  # Valide la transaction
            return True
        except SQLAlchemyError as e:
            session.rollback()  # Annule la transaction en cas d'erreur
            logging.error(f"Erreur lors de la création de l'utilisateur : {e}")
            return False
        finally:
            session.close()

    @log
    def trouver_par_id(self, id_user) -> Utilisateur:
        """Trouver un utilisateur grâce à son ID

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur à chercher

        Returns
        -------
        utilisateur : Utilisateur
            L'utilisateur trouvé, ou None si non trouvé
        """
        session = self.Session()
        try:
            utilisateur = session.query(Utilisateur).filter_by(id_user=id_user).first()
            return utilisateur
        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la recherche de l'utilisateur : {e}")
            return None
        finally:
            session.close()

    @log
    def lister_tous(self) -> list[Utilisateur]:
        """Lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateur]
            Liste de tous les utilisateurs dans la base de données
        """
        session = self.Session()
        try:
            utilisateurs = session.query(Utilisateur).all()
            return utilisateurs
        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []
        finally:
            session.close()

    @log
    def modifier(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        modified : bool
            True si la modification a été réussie
            False sinon
        """
        session = self.Session()
        try:
            existing_user = (
                session.query(Utilisateur).filter_by(id_user=utilisateur.id_user).first()
            )
            if existing_user:
                existing_user.nom_user = utilisateur.nom_user
                existing_user.mail_user = utilisateur.mail_user
                existing_user.mdp = utilisateur.mdp
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Erreur lors de la modification de l'utilisateur : {e}")
            return False
        finally:
            session.close()

    @log
    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            Utilisateur à supprimer

        Returns
        -------
        bool : True si l'utilisateur a été supprimé, False sinon
        """
        session = self.Session()
        try:
            existing_user = (
                session.query(Utilisateur).filter_by(id_user=utilisateur.id_user).first()
            )
            if existing_user:
                session.delete(existing_user)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return False
        finally:
            session.close()

    @log
    def se_connecter(self, nom_user, mdp) -> Utilisateur:
        """Se connecter avec le nom d'utilisateur et le mot de passe

        Parameters
        ----------
        nom_user : str
            Nom d'utilisateur de l'utilisateur qui souhaite se connecter
        mdp : str
            Mot de passe de l'utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            L'utilisateur trouvé, ou None si l'authentification échoue
        """
        session = self.Session()
        try:
            utilisateur = session.query(Utilisateur).filter_by(nom_user=nom_user, mdp=mdp).first()
            if utilisateur:
                session.expunge(utilisateur)  # détache explicitement l’objet de la session
            return utilisateur
        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la connexion de l'utilisateur : {e}")
            return None
        finally:
            session.close()

