from business_object.Activity_object.abstract_activity import AbstractActivity


class Natation(AbstractActivity):
    """Activité de natation"""

    def __init__(
        self,
        id_activite,
        titre,
        description,
        date_activite,
        duree,
        distance,
        id_user,
        type_nage: str,
    ):
        super().__init__(id_activite, titre, description, date_activite, duree, distance, id_user)
        self.type_nage = type_nage

    def vitesse(self):
        """
        Dans la nage, la vitesse est souvent mesurée en mètres par seconde (m/s).
        Calcule la vitesse en m/s (mètres par seconde)
        Returns:
            float: vitesse en m/s
        """
        if self.duree > 0:
            # distance en km, durée en minutes -> vitesse en m/s
            # Conversion: km -> m (*1000) et minutes -> secondes (*60)
            return (self.distance * 1000) / (self.duree * 60)
        return 0

    def __str__(self):
        return f"{self.type_nage} - {super().__str__()} - Vitesse moyenne: {self.vitesse():.2f} m/s"
