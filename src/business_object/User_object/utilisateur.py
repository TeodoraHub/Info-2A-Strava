from datetime import datetime

import gpxpy

from business_object.Activity_object.abstract_activity import Activite
from business_object.Activity_object.course_pied import CoursePied
from business_object.Activity_object.cyclism import Cyclism
from business_object.Activity_object.natation import Natation
from business_object.Activity_object.randonnee import Randonnee


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

        # Ces fonctions sont faîtes en partant du principe qu'on a une liste des activités dans les attributs

        def consulter_activites(self):
            return self.activites

        def supprimer_activite(self):
            self.activites = [a for a in self.activites if a.id_activite != id_activite]
