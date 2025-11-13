from business_object.Activity_object.abstract_activity import AbstractActivity


class Cyclisme(AbstractActivity):
    def __init__(
        self,
        id_activite,
        titre,
        description,
        date_activite,
        lieu: str,
        distance,
        id_user,
        duree: float | None = None,
        type_velo: str | None = None,
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
            duree=duree,
        )
        self.type_velo = type_velo

    def vitesse(self) -> float:
        """Vitesse moyenne en km/h."""
        if self.duree and self.duree > 0:
            return (self.distance / self.duree) * 60
        return 0.0

    def __str__(self):
        return (
            f"{self.type_velo} - {super().__str__()} - Vitesse moyenne: {self.vitesse():.2f} km/h"
        )
