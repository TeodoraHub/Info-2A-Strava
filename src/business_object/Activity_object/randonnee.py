from business_object.Activity_object.abstract_activity import AbstractActivity

class Randonnee(AbstractActivity):
    __tablename__ = 'activite'  # Nom de la table dans la base de données
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {
        'polymorphic_identity': 'randonnee',  # Identifiant pour le polymorphisme
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
        type_terrain: str = None,
    ):
        super().__init__(
            id=id_activite,
            titre=titre,
            description=description,
            sport="randonnee",
            date_activite=date_activite,
            lieu=lieu,
            distance=distance,
            id_user=id_user,
            duree=duree
        )
        self.type_terrain = type_terrain

    def vitesse(self) -> float:
        """
        Calcule la vitesse en km/h
        Return:
            float: vitesse en km/h
        """
        if self.duree and self.duree > 0:
            # distance en km, durée en minutes -> vitesse en km/h
            return (self.distance / self.duree) * 60
        return 0.0

    def __str__(self):
        return f"Randonnée - {self.type_terrain} - {super().__str__()} - Vitesse moyenne : {self.vitesse():.2f} km/h"
