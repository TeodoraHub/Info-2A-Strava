from business_object.Activity_object.abstract_activity import AbstractActivity


class Natation(AbstractActivity):
    """Activité de natation"""

    def __init__(
        self,
        id_activite,
        titre,
        description,
        date_activite,
        lieu: str,
        distance: float,
        id_user: int,
        type_nage: str,
        duree: float = None,
    ):
        super().__init__(
            id=id_activite,
            titre=titre,
            description=description,
            sport="natation",
            date_activite=date_activite,
            lieu=lieu,
            distance=distance,
            id_user=id_user,
            duree=duree
        )
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
