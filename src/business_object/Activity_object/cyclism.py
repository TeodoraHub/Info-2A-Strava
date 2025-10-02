from datetime import date

from business_object.Activity_object.abstract_activity import AbstractActivity


class Cyclism(AbstractActivity):
    def __init__(
        self,
        titre,
        description,
        date_activite: date,
        distance,
        id_user,
        type_velo: str,
    ):
        super().__init__(id, titre, description, date_activite, distance, id_user)
        self.type_velo = type_velo

    def __str__(self):
        return f" {self.type_velo} - {super().__str__()}"
