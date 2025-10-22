from datetime import datetime

import gpxpy

from business_object.Activity_object.abstract_activity import Activite
from business_object.Activity_object.course_a_pieds import CoursePied
from business_object.Activity_object.cyclism import Cyclism
from business_object.Activity_object.natation import Natation
from business_object.Activity_object.randonnee import Randonnee
from dao.activite_dao import ActivityDAO

class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_user : int
        identifiant
    nom_user : str
        nom de l'utilisateur
    mail_user : str
        adresse mail de l'utilisateur
    mdp : str
        le mot de passe de l'utilisateur
    """

    def __init__(self, id_user, nom_user, mail_user, mdp):
        """Constructeur"""
        self.id_user = id_user
        self.nom_user = nom_user
        self.mail_user = mail_user
        self.mdp = mdp
        # On fait une fausse liste d'activité pour l'instant mais on devra la relier à la base de données après
        self.activites: list[Activite] = []

    def __str__(self):
        """Permet d'afficher les informations de l'utilisateur"""
        return f"Utilisateur({self.nom_user}, {self.mail_user})"

    def as_list(self) -> list[str]:
        """Retourne les attributs de l'utilisateur dans une liste"""
        return [self.id_user, self.nom_user, self.mail_user]

    def creer_activite(
        self,
        type_activite: str,
        titre: str,
        description: str,
        lieu: str,
        fichier_gpx: str,
        **kwargs,
    ):
        """
        Permet de créer une nouvelle activité

        Parameters
        ----------
        type_activite : str
            type de l'activité (course, cyxlisme, natation ou randonnee)
        titre : str
            titre de l'activité
        description : str
            desription de l'activité
        lieu : str
            lieu de l'activité
        fichier_gpx : str
            fichier contenant les informations sur l'activité

        Returns
        -------
        return : AbstractActivity
            renvoie l'activité créée
        """
        with open(fichier_gpx, "r", encoding="utf-8") as f:
            gpx = gpxpy.parse(f)

        distance_m = gpx.length_3d()
        duree = gpx.get_duration()

        # Génération d’un id d’activité arbitraire
        id_activite = int(datetime.now().timestamp())

        if type_activite == "course":
            return CoursePied(
                id_activite=id_activite,
                titre=titre,
                description=description,
                date_activite=datetime.now(),
                duree=duree,
                distance=distance_m,
                id_user=self.id_user,
            )

        elif type_activite == "cyclisme":
            type_velo = kwargs.get("type_velo", "route")
            return Cyclism(
                titre=titre,
                description=description,
                date_activite=datetime.now().date(),
                distance=distance_m,
                id_user=self.id_user,
                type_velo=type_velo,
            )

        elif type_activite == "natation":
            type_nage = kwargs.get("type_nage", "crawl")
            return Natation(
                id_activite=id_activite,
                titre=titre,
                description=description,
                date_activite=datetime.now(),
                duree=duree,
                distance=distance_m,
                id_user=self.id_user,
                type_nage=type_nage,
            )

        elif type_activite == "randonnee":
            type_terrain = kwargs.get("type_terrain", "sentier")
            return Randonnee(
                id_activite=id_activite,
                titre=titre,
                description=description,
                date_activite=datetime.now(),
                duree=duree,
                distance=distance_m,
                id_user=self.id_user,
                type_terrain=type_terrain,
            )

        else:
            raise ValueError(f"Type d’activité inconnu: {type_activite}")


    def consulter_activites(self):
        """
        Liste toutes les activités appartenant à l'utilisateur,
        en interrogeant la base via ActivityDAO.
        """
        utilisateur = Session().utilisateur
        if not utilisateur or utilisateur.db_session is None:
            raise RuntimeError("Aucun utilisateur connecté.")

        dao = ActivityDAO(session)
        activites = dao.get_by_user(self.id_user)
        return activites


    def modifier_activite(self):
        """
        Permet à l'utilisateur de modifier une de ses activités.

        Fonctionnement
        -------------
        1. Liste toutes les activités de l'utilisateur avec leur ID et titre.
        2. Demande à l'utilisateur de saisir l'ID de l'activité à modifier.
        3. Permet de modifier le titre et la description (les champs laissés vides restent inchangés).
        4. Enregistre les modifications dans la base de données.

        Raises
        ------
        ValueError
            si l'ID saisi ne correspond à aucune activité de l'utilisateur
        RuntimeError
            si aucune session SQLAlchemy n'est associée à l'utilisateur
        """
        utilisateur = Session().utilisateur
        if not utilisateur or utilisateur.db_session is None:
            raise RuntimeError("Aucun utilisateur connecté.")

        dao = ActivityDAO(self.db_session)
        activites = dao.get_by_user(self.id_user)
        if not activites:
            print("Aucune activité à modifier.")
            return

        # Affiche les activités avec leur ID
        for act in activites:
            print(f"ID {act.id}: {act.titre}")

        choix_id = int(input("Entrez l'ID de l'activité à modifier : "))
        activite = next((a for a in activites if a.id == choix_id), None)
        if not activite:
            print("ID invalide.")
            return

        # Demande les champs à modifier
        nouveau_titre = input(f"Titre ({activite.titre}): ") or activite.titre
        nouvelle_description = input(f"Description ({activite.description}): ") or activite.description

        activite.titre = nouveau_titre
        activite.description = nouvelle_description

        self.db_session.commit()
        print("Activité modifiée.")


    def supprimer_activite(self):
        """
        Permet à l'utilisateur de supprimer une de ses activités.

        Fonctionnement
        -------------
        1. Liste toutes les activités de l'utilisateur avec leur ID et titre.
        2. Demande à l'utilisateur de saisir l'ID de l'activité à supprimer.
        3. Supprime l'activité de la base de données.

        Raises
        ------
        ValueError
            si l'ID saisi ne correspond à aucune activité de l'utilisateur
        RuntimeError
            si aucune session SQLAlchemy n'est associée à l'utilisateur
        """
        utilisateur = Session().utilisateur
        if not utilisateur or utilisateur.db_session is None:
            raise RuntimeError("Aucun utilisateur connecté.")

        dao = ActivityDAO(self.db_session)
        activites = dao.get_by_user(self.id_user)
        if not activites:
            print("Aucune activité à supprimer.")
            return

        # Affiche les activités avec leur ID
        for act in activites:
            print(f"ID {act.id}: {act.titre}")

        choix_id = int(input("Entrez l'ID de l'activité à supprimer : "))
        activite = next((a for a in activites if a.id == choix_id), None)
        if not activite:
            raise ValueError("ID invalide : aucune activité correspondante.")

        self.db_session.delete(activite)
        self.db_session.commit()
        print("Activité supprimée.")

    def suivre_utilisateur(self, utilisateur_a_suivre):
        """
        Permet à l'utilisateur connecté de suivre un autre utilisateur.

        Parameters
        ----------
        utilisateur_a_suivre : Utilisateur
            instance de l'utilisateur à suivre

        Raises
        ------
        ValueError
            si l'utilisateur se suit lui-même ou est déjà suivi
        """
        utilisateur = Session().utilisateur
        if utilisateur.id_user == utilisateur_a_suivre.id_user:
            raise ValueError("Impossible de se suivre soi-même.")

        dao = SuiviDAO(utilisateur.db_session)
        suivi_existant = dao.existe_suivi(utilisateur.id_user, utilisateur_a_suivre.id_user)
        if suivi_existant:
            raise ValueError("Utilisateur déjà suivi.")

        dao.ajouter_suivi(utilisateur.id_user, utilisateur_a_suivre.id_user)


def liker_activite(self, activite):
    """
    Permet à l'utilisateur connecté de liker une activité,
    en vérifiant dans la base que le like n'existe pas déjà.

    Parameters
    ----------
    activite : Activity
        instance de l'activité à liker

    Returns
    -------
    Like
        objet Like créé
    """
    utilisateur = Session().utilisateur
    dao = LikeDAO(utilisateur.db_session)

    # Vérifie si l'utilisateur a déjà liké l'activité
    if dao.existe_like(utilisateur.id_user, activite.id):
        print("Vous avez déjà liké cette activité.")
        return None

    # Crée le like dans la base
    like = Like(
        id_activite=activite.id,
        id_user=utilisateur.id_user,
        date_like=datetime.now()
    )
    dao.ajouter_like(like)
    return like


def commenter_activite(self, activite, contenu: str):
    """
    Permet à l'utilisateur connecté de commenter une activité,
    en enregistrant le commentaire directement dans la base.

    Parameters
    ----------
    activite : Activity
        instance de l'activité à commenter
    contenu : str
        texte du commentaire

    Returns
    -------
    Commentaire
        objet Commentaire créé et stocké en base
    """
    utilisateur = Session().utilisateur
    dao = CommentaireDAO(utilisateur.db_session)

    commentaire = Commentaire(
        id_activite=activite.id,
        contenu=contenu,
        date_commentaire=datetime.now(),
        id_user=utilisateur.id_user
    )

    dao.ajouter_commentaire(commentaire)
    return commentaire


    def obtenir_statistiques(self, periode: str = None, sport: str = None):
        """
        Retourne les statistiques de l'utilisateur connecté.

        Parameters
        ----------
        periode : str, optional
            période à filtrer ('7j' ou '30j')
        sport : str, optional
            sport à filtrer ('course', 'cyclisme', 'natation', 'randonnee')

        Returns
        -------
        dict
            dictionnaire avec nombre d'activités, kilomètres et heures
        """
        utilisateur = Session().utilisateur
        stats = {
            "nombre_activites": Statistiques.nombre_activites(utilisateur, periode, sport),
            "kilometres": Statistiques.kilometres(utilisateur, periode, sport),
            "heures": Statistiques.heures_activite(utilisateur, periode, sport)
        }
        return stats
