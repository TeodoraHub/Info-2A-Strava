from abc import ABC, abstractmethod
from datetime import date


class AbstractActivity(ABC):
    def __init__(
        self,
        id: int,
        titre: str,
        description: str,
        sport: str,
        date_activite: date,
        lieu: str,
        distance: float,
        id_user: int,
        duree: float = None,
    ):
        self.id = id
        self.titre = titre
        self.description = description
        self.sport = sport
        self.date_activite = date_activite
        self.lieu = lieu
        self.distance = distance
        self.id_user = id_user
        self.duree = duree

    def __str__(self):
        return f"{self.titre} - {self.date_activite} - {self.distance}km"

    @abstractmethod
    def vitesse(self) -> float:
        """
        calculer et retourner la vitesse de l'activité.
        """
        pass
