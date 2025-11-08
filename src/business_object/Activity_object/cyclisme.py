from business_object.Activity_object.abstract_activity import AbstractActivity


class Cyclisme(AbstractActivity):
    __tablename__ = "activite"  # Nom de la table dans la base de données
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {
        "polymorphic_identity": "cyclisme",  # Identifiant pour le polymorphisme
        "polymorphic_on": "sport",  # Colonne utilisée pour le polymorphisme
    }

    def __init__(
        self,
        *,
        id_activite,
        titre,
        description,
        date_activite,
        lieu: str,
        distance,
        id_user,
        duree: float = None,
        type_velo: str = None,
    ):
        super().__init__(
            id_activite=id_activite,
            titre=titre,
            description=description,
            sport="cyclisme",
            date_activite=date_activite,
            lieu=lieu,
            distance=distance,
            id_user=id_user,
            duree=duree,
        )
        self.type_velo = type_velo

    def vitesse(self) -> float:
        """
        Calcule la vitesse en km/h
        Return:
            float: vitesse en km/h
        """
        if self.duree and self.duree > 0:
            # Pour une distance en km et une durée en minutes
            return (self.distance / self.duree) * 60
        return 0.0

    def __str__(self):
        return (
            f"{self.type_velo} - {super().__str__()} - Vitesse moyenne: {self.vitesse():.2f} km/h"
        )
