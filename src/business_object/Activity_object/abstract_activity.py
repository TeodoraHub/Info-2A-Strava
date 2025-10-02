from abc import ABC
from datetime import date


class AbstractActivity(ABC):
    def __init__(
        self,
        id: int,
        titre: str,
        description: str,
        date_activite: date,
        lieu: str,
        distance: float,
        id_user: int,
    ):
        self.id = id
        self.titre = titre
        self.description = description
        self.date_activite = date_activite
        self.lieu = lieu
        self.distance = distance
        self.id_user = id_user

    def __str__(self):
        return f"{self.titre} - {self.date_activite} - {self.distance}km en {self.duree}min"
