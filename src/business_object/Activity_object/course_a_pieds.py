from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
    __mapper_args__ = {"polymorphic_identity": "course"}

    def __init__(
        self,
        *,
        id_activite,
        titre,
        description,
        date_activite,
        lieu,
        distance,
        id_user,
        duree=None,
    ):
        super().__init__(
            id_activite=id_activite,
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
            return self.distance / self.duree
        return 0.0
