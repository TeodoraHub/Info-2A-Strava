from datetime import datetime

from utils.singleton import Singleton


class Session(metaclass=Singleton):
    """Stocke les données liées à une session."""

    def __init__(self):
        self.utilisateur = None
        self.debut_connexion = None

    def connexion(self, utilisateur):
        self.utilisateur = utilisateur
        self.debut_connexion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        self.utilisateur = None
        self.debut_connexion = None

    def afficher(self) -> str:
        res = "Actuellement en session :\n"
        res += "-------------------------\n"
        for att in list(self.__dict__.items()):
            res += f"{att[0]} : {att[1]}\n"
        return res

    @classmethod
    def reset(cls):
        """Réinitialise l'instance Singleton de Session."""
        instance = Singleton._instances.get(cls)
        if instance is not None:
            instance.__init__()
            del Singleton._instances[cls]
