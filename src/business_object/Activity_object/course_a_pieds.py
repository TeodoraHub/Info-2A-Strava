from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
    """Activité de course à pied"""

    def __init__(self, id_activite, titre, description, date_activite, duree, distance, id_user):
        super().__init__(id_activite, titre, description, date_activite, duree, distance, id_user)

    def __str__(self):
        return f" {self.get_type_activite()} - {super().__str__()}"

    def vitesse(self) -> float:
        """Calculer et retourner la vitesse de l'activité en km/h.
        return : vitesse moyenne en km/h
        """
        if self.duree == 0:
            return 0.0
        return self.distance / self.duree
