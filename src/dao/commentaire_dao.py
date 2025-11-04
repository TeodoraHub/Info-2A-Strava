import logging
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table, create_engine
from sqlalchemy.sql import delete, func, insert, select, update

from business_object.like_comment_object.commentaire import Commentaire
from utils.log_decorator import log
from utils.singleton import Singleton

# URL de la base de données (à adapter selon votre configuration)
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Création du moteur de connexion
engine = create_engine(DATABASE_URL)

# Création d'une instance de MetaData
metadata = MetaData()

# Définition de la table `commentaire`
commentaire_table = Table(
    "commentaire",
    metadata,
    Column("id_comment", Integer, primary_key=True, autoincrement=True),
    Column("id_user", Integer, ForeignKey("utilisateur.id_user"), nullable=False),
    Column("id", Integer, ForeignKey("activite.id"), nullable=False),  # id_activite
    Column("contenu", String, nullable=False),
    Column("date_comment", DateTime, nullable=False),
)


class CommentaireDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Commentaires de la base de données"""

    @log
    def creer_commentaire(self, id_user: int, id_activite: int, contenu: str) -> Commentaire:
        """Création d'un commentaire dans la base de données.

        Parameters
        ----------
        id_user : int
            Identifiant de l'utilisateur.
        id_activite : int
            Identifiant de l'activité.
        contenu : str
            Contenu du commentaire.

        Returns
        -------
        Commentaire
            Objet Commentaire créé.
        """
        try:
            # Création de la requête d'insertion
            stmt = (
                insert(commentaire_table)
                .values(
                    id_user=id_user, id=id_activite, contenu=contenu, date_comment=datetime.now()
                )
                .returning(commentaire_table.c.id_comment)
            )

            # Exécution de la requête
            with engine.connect() as connection:
                result = connection.execute(stmt)
                id_comment = result.fetchone()[0]  # Récupère l'id_comment généré
                connection.commit()

            # Récupération du commentaire nouvellement créé
            commentaire = Commentaire(
                id_activite=id_activite,
                contenu=contenu,
                date_commentaire=datetime.now(),
                id_user=id_user,
                id_comment=id_comment,
            )

            return commentaire
        except Exception as e:
            logging.error(f"Erreur lors de la création du commentaire: {e}")
            return None

    @log
    def supprimer_commentaire(self, id_comment) -> bool:
        """Suppression d'un commentaire dans la base de données

        Parameters
        ----------
        id_comment : int
            identifiant du commentaire

        Returns
        -------
        deleted : bool
            True si la suppression est un succès
            False sinon
        """
        try:
            stmt = delete(commentaire_table).where(commentaire_table.c.id_comment == id_comment)
            with engine.connect() as connection:
                result = connection.execute(stmt)
                connection.commit()
            return result.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du commentaire: {e}")
            return False

    @log
    def get_commentaires_by_activity(self, id_activite) -> list[Commentaire]:
        """Récupère tous les commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        liste_commentaires : list[Commentaire]
            liste des commentaires de l'activité
        """
        try:
            stmt = (
                select(commentaire_table)
                .where(commentaire_table.c.id == id_activite)
                .order_by(commentaire_table.c.date_comment.desc())
            )
            with engine.connect() as connection:
                result = connection.execute(stmt)
                rows = result.fetchall()

            liste_commentaires = []
            for row in rows:
                commentaire = Commentaire(
                    id_comment=row["id_comment"],
                    id_user=row["id_user"],
                    id_activite=row["id"],
                    contenu=row["contenu"],
                    date_commentaire=row["date_comment"],
                )
                liste_commentaires.append(commentaire)
            return liste_commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def get_commentaires_by_user(self, id_user) -> list[Commentaire]:
        """Récupère tous les commentaires d'un utilisateur

        Parameters
        ----------
        id_user : int
            identifiant de l'utilisateur

        Returns
        -------
        liste_commentaires : list[Commentaire]
            liste des commentaires de l'utilisateur
        """

        try:
            stmt = (
                select(commentaire_table)
                .where(commentaire_table.c.id_user == id_user)
                .order_by(commentaire_table.c.date_comment.desc())
            )
            with engine.connect() as connection:
                result = connection.execute(stmt)
                rows = result.fetchall()

            liste_commentaires = []
            for row in rows:
                commentaire = Commentaire(
                    id_comment=row["id_comment"],
                    id_user=row["id_user"],
                    id_activite=row["id"],
                    contenu=row["contenu"],
                    date_commentaire=row["date_comment"],
                )
                liste_commentaires.append(commentaire)
            return liste_commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires: {e}")
            return []

    @log
    def count_commentaires_by_activity(self, id_activite) -> int:
        """Compte le nombre de commentaires d'une activité

        Parameters
        ----------
        id_activite : int
            identifiant de l'activité

        Returns
        -------
        count : int
            nombre de commentaires de l'activité
        """

        try:
            stmt = (
                select([func.count()])
                .select_from(commentaire_table)
                .where(commentaire_table.c.id == id_activite)
            )
            with engine.connect() as connection:
                result = connection.execute(stmt)
                count = result.scalar()
            return count if count is not None else 0
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires: {e}")
            return 0

    @log
    def modifier_commentaire(self, id_comment, nouveau_contenu) -> bool:
        """Modification d'un commentaire dans la base de données

        Parameters
        ----------
        id_comment : int
            identifiant du commentaire
        nouveau_contenu : str
            nouveau contenu du commentaire

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """

        try:
            stmt = (
                update(commentaire_table)
                .where(commentaire_table.c.id_comment == id_comment)
                .values(contenu=nouveau_contenu)
            )
            with engine.connect() as connection:
                result = connection.execute(stmt)
                connection.commit()
            return result.rowcount == 1
        except Exception as e:
            logging.error(f"Erreur lors de la modification du commentaire: {e}")
            return False
