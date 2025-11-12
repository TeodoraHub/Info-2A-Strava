from datetime import datetime

import gpxpy

from business_object.Activity_object.course_a_pieds import CoursePied
from business_object.Activity_object.cyclisme import Cyclisme
from business_object.Activity_object.natation import Natation
from business_object.Activity_object.randonnee import Randonnee
from business_object.user_object.statistiques import Statistiques

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Utilisateur(Base):
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
    __tablename__ = "utilisateur"
    id_user = Column(Integer, primary_key=True)
    nom_user = Column(String)
    mail_user = Column(String)
    mdp = Column(String)

    def __init__(self, id_user, nom_user, mail_user, mdp):
        self.id_user = id_user
        self.nom_user = nom_user
        self.mail_user = mail_user
        self.mdp = mdp

    def __str__(self):
        return f"Utilisateur({self.nom_user}, {self.mail_user})"

    def as_list(self) -> list[str]:
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

        id_activite = int(datetime.now().timestamp())

        if type_activite == "course":
            return CoursePied(
                id_activite=id_activite,
                titre=titre,
                description=description,
                date_activite=datetime.now(),
                lieu=lieu,
                duree=duree,
                distance=distance_m,
                id_user=self.id_user,
            )

        elif type_activite == "cyclisme":
            type_velo = kwargs.get("type_velo", "route")
            return Cyclisme(
                id_activite=id_activite,
                titre=titre,
                description=description,
                date_activite=datetime.now(),
                lieu=lieu,
                duree=duree,
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
                lieu=lieu,
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
                lieu=lieu,
                duree=duree,
                distance=distance_m,
                id_user=self.id_user,
                type_terrain=type_terrain,
            )

        else:
            raise ValueError(f"Type d’activité inconnu: {type_activite}")

    def obtenir_statistiques(self, periode: str = None, sport: str = None):
        stats = {
            "nombre_activites": Statistiques.nombre_activites(self, periode, sport),
            "kilometres": Statistiques.kilometres(self, periode, sport),
            "heures": Statistiques.heures_activite(self, periode, sport),
        }
        return stats
