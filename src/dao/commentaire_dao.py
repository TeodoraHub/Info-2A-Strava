import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from business_object.like_comment_object.commentaire import Commentaire
from utils.log_decorator import log
from utils.singleton import Singleton

# URL de la base de données (à adapter selon votre configuration)
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Création du moteur de connexion
engine = create_engine(DATABASE_URL)


# Classe CommentaireDAO avec Singleton
class CommentaireDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""

    def __init__(self, session: Session):
        self.session = session  # Session SQLAlchemy

    @log
    def creer_commentaire(self, id_user: int, id_activite: int, contenu: str) -> Commentaire:
        """Création d'un commentaire dans la base de données."""
        try:
            commentaire = Commentaire(
                id_user=id_user,
                id_activite=id_activite,
                contenu=contenu,
                date_commentaire=datetime.now(),
            )
            self.session.add(commentaire)
            self.session.commit()  # Validation de la transaction
            return commentaire
        except Exception as e:
            self.session.rollback()  # Annuler en cas d'erreur
            logging.error(f"Erreur lors de la création du commentaire: {e}")
            return None

    @log
    def supprimer_commentaire(self, id_comment: int) -> bool:
        """Suppression d'un commentaire dans la base de données."""
        try:
            commentaire = self.session.query(Commentaire).filter_by(id_comment=id_comment).first()
            if commentaire:
                self.session.delete(commentaire)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erreur lors de la suppression du commentaire: {e}")
            return False

    @log
    def get_commentaires_by_activity(self, id_activite: int) -> list[Commentaire]:
        """Récupère tous les commentaires d'une activité."""
        try:
            commentaires = (
                self.session.query(Commentaire)
                .filter_by(id_activite=id_activite)
                .order_by(Commentaire.date_commentaire.desc())
                .all()
            )
            return commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def get_commentaires_by_user(self, id_user: int) -> list[Commentaire]:
        """Récupère tous les commentaires d'un utilisateur."""
        try:
            commentaires = (
                self.session.query(Commentaire)
                .filter_by(id_user=id_user)
                .order_by(Commentaire.date_commentaire.desc())
                .all()
            )
            return commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def count_commentaires_by_activity(self, id_activite: int) -> int:
        """Compte le nombre de commentaires d'une activité."""
        try:
            count = self.session.query(Commentaire).filter_by(id_activite=id_activite).count()
            return count
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires: {e}")
            return 0

    @log
    def modifier_commentaire(self, id_comment: int, nouveau_contenu: str) -> bool:
        """Modification d'un commentaire dans la base de données."""
        try:
            commentaire = self.session.query(Commentaire).filter_by(id_comment=id_comment).first()
            if commentaire:
                commentaire.contenu = nouveau_contenu
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            logging.error(f"Erreur lors de la modification du commentaire: {e}")
            return False
            logging.error(f"Erreur lors de la modification du commentaire: {e}")
            return False
