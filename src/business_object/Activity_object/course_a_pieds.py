from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
    """Activité de course à pied"""

    def __init__(
        self, 
        id_activite, 
        titre, 
        description, 
        date_activite,
        lieu: str, 
        distance, 
        id_user,
        duree: float = None,
        ):
        super().__init__(
            id=id_activite,
            titre=titre,
            description=description,
            sport="course",
            date_activite=date_activite,
            lieu=lieu,
            distance=distance,
            id_user=id_user,
            duree=duree
            )

    def __str__(self):
        return f" {self.get_type_activite()} - {super().__str__()}"

    def vitesse(self) -> float:
        """Calculer et retourner la vitesse de l'activité en km/h.
        return : vitesse moyenne en km/h
        """
        if self.duree == 0:
            return 0.0
        return self.distance / self.duree
