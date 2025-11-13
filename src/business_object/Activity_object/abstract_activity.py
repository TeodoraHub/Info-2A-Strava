from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class AbstractActivity(ABC):
    """Modèle métier d'activité (sans mapping ORM).

    Attributs communs aux différentes activités (course, cyclisme, natation, randonnée).
    """

    def __init__(
        self,
        id: int,
        titre: str,
        description: str,
        sport: str,
        date_activite: datetime,
        lieu: str,
        distance: float,
        id_user: int,
        duree: Optional[float] = None,
    ) -> None:
        self.id = id
        self.titre = titre
        self.description = description
        self.sport = sport
        self.date_activite = date_activite
        self.lieu = lieu
        self.distance = float(distance)
        self.duree = duree
        self.id_user = id_user

    @abstractmethod
    def vitesse(self) -> float:
        """Calcule la vitesse moyenne de l'activité.

        La convention des unités est laissée à la sous-classe
        (km/h pour course/cyclisme/randonnée, m/s pour natation).
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.titre} - {self.sport}"
