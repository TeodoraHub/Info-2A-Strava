from business_object.Activity_object.abstract_activity import AbstractActivity

class Natation(AbstractActivity):
    __tablename__ = 'activite'  # Nom de la table dans la base de données
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {
        'polymorphic_identity': 'natation',  # Identifiant pour le polymorphisme
        'polymorphic_on': 'sport'  # Colonne utilisée pour le polymorphisme
    }

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
        type_nage: str = None,
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

    def vitesse(self) -> float:
        """
        Calcule la vitesse en m/s (mètres par seconde)
        Returns:
            float: vitesse en m/s
        """
        if self.duree and self.duree > 0:
            # distance en km, durée en minutes -> vitesse en m/s
            return (self.distance * 1000) / (self.duree * 60)
        return 0.0

    def __str__(self):
        return f"{self.type_nage} - {super().__str__()} - Vitesse moyenne: {self.vitesse():.2f} m/s"
