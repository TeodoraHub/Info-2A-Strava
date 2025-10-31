from datetime import date

from business_object.Activity_object.abstract_activity import AbstractActivity


class Cyclisme(AbstractActivity):
    def __init__(
        self,
        id_activite,
        titre,
        description,
        duree,
        date_activite: date,
        lieu: str,
        distance,
        id_user,
        type_velo: str,
    ):
        super().__init__(
            id=id_activite,
            titre=titre,
            description=description,
            sport="cyclisme",
            date_activite=date_activite,
            lieu=lieu,
            distance=distance,
            id_user=id_user,
            duree=duree
        )
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
