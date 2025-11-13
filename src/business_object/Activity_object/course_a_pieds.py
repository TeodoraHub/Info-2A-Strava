from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
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
            duree=duree,
        )

    def vitesse(self) -> float:
        if self.duree and self.duree > 0:
            return (self.distance / self.duree) * 60  # km/h
        return 0.0
