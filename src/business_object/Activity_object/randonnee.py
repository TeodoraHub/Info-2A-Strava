from business_object.Activity_object.abstract_activity import AbstractActivity


class Randonnee(AbstractActivity):
    """Activité de randonnée"""

    def __init__(
        self,
        id_activite,
        titre,
        description,
        date_activite,
        duree,
        distance,
        id_user,
        type_terrain: str,
    ):
        super().__init__(id_activite, titre, description, date_activite, duree, distance, id_user)
        self.type_terrain = type_terrain

    def __str__(self):
        return f" Randonnée - {self.type_terrain} - {super().__str__()}"
