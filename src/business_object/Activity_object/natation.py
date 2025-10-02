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

    def __str__(self):
        return f" {self.type_nage} - {super().__str__()}"
