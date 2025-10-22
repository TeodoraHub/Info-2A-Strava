from datetime import date

from business_object.Activity_object.abstract_activity import AbstractActivity


class Cyclisme(AbstractActivity):
    def __init__(
        self,
        titre,
        duree,
        description,
        date_activite: date,
        distance,
        id_user,
        type_velo: str,
    ):
        super().__init__(id, titre, description, date_activite, duree, distance, id_user)
        self.type_velo = type_velo

    def vitesse(self):
        """
        Calcule la vitesse en km/h
        Return:
            float: vitesse en km/h
        """
        if self.duree > 0:
            # pour une distance en km et une durée en minutes
            return (self.distance / self.duree) * 60
        return 0

    def __str__(self):
        return (
            f"{self.type_velo} - {super().__str__()} - Vitesse moyenne: {self.vitesse():.2f} km/h"
        )
