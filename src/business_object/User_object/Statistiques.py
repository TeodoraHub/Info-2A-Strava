from datetime import datetime, timedelta


class Statistiques:
    """
    Classe utilitaire pour calculer des statistiques
    sur les activités d'un utilisateur, sans stocker d'état.

    Toutes les méthodes sont statiques et prennent un objet
    Utilisateur en paramètre.
    """

    @staticmethod
    def nombre_activites(utilisateur, periode: str = None, sport: str = None) -> int:
        """
        Retourne le nombre d'activités de l'utilisateur
        selon une période et un sport donnés.
        """
        activites = Statistiques._filtrer(utilisateur, periode, sport)
        return len(activites)

    @staticmethod
    def kilometres(utilisateur, periode: str = None, sport: str = None) -> float:
        """
        Retourne le total des kilomètres parcourus par l'utilisateur.
        """
        activites = Statistiques._filtrer(utilisateur, periode, sport)
        return sum(getattr(a, "distance", 0) for a in activites) / 1000

    @staticmethod
    def heures_activite(utilisateur, periode: str = None, sport: str = None) -> float:
        """
        Retourne le total des heures d'activité de l'utilisateur.
        """
        activites = Statistiques._filtrer(utilisateur, periode, sport)
        return sum(getattr(a, "duree", 0) for a in activites) / 3600

    @staticmethod
    def _filtrer(utilisateur, periode: str = None, sport: str = None):
        """
        Filtre les activités de l'utilisateur selon une période et un sport.
        """
        activites = getattr(utilisateur, "activites", [])

        if sport:
            activites = [a for a in activites if a.__class__.__name__.lower() == sport.lower()]

        if periode == "7j":
            seuil = datetime.now() - timedelta(days=7)
            activites = [a for a in activites if a.date_activite >= seuil]
        elif periode == "30j":
            seuil = datetime.now() - timedelta(days=30)
            activites = [a for a in activites if a.date_activite >= seuil]

        return activites
        return activites
