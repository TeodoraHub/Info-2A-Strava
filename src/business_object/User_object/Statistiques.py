from datetime import datetime, timedelta


class Statistiques:
    """
    Classe permettant de calculer des statistiques
    sur les activités d'un utilisateur.

    Attributs
    ----------
    utilisateur : Utilisateur
        l'utilisateur dont on veut calculer les statistiques
    """

    def __init__(self, utilisateur):
        """Constructeur"""
        self.utilisateur = utilisateur

    def __str__(self):
        """Affichage simplifié"""
        return f"Statistiques de {self.utilisateur.nom_user}"

    def nombre_activites(self, periode: str = None, sport: str = None) -> int:
        """
        Retourne le nombre d'activités selon une période et un sport donnés.

        Paramètres
        ----------
        periode : str, optionnel
            "7j", "30j" ou None (par défaut : toutes les activités)
        sport : str, optionnel
            type de sport (CoursePied, Cyclism, Natation, Randonnee)

        Retour
        ------
        int
        """
        activites = self._filtrer(periode, sport)
        return len(activites)

    def kilometres(self, periode: str = None, sport: str = None) -> float:
        """
        Retourne le total des kilomètres parcourus.
        """
        activites = self._filtrer(periode, sport)
        return sum(getattr(a, "distance", 0) for a in activites) / 1000

    def heures_activite(self, periode: str = None, sport: str = None) -> float:
        """
        Retourne le total des heures d'activité.
        """
        activites = self._filtrer(periode, sport)
        return sum(getattr(a, "duree", 0) for a in activites) / 3600

    def _filtrer(self, periode: str, sport: str):
        """
        Filtre les activités de l'utilisateur selon période et sport.
        """
        activites = getattr(self.utilisateur, "activites", [])

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
