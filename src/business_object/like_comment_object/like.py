class Like:
    """
    Classe représentant un like

    Attributs
    ----------
    id_activite : int
        identifiant de l'activité
    id_user : int
        identifiant de l'utilisateur qui like l'activité
    date_like : Date
        date du like
    """

    def __init__(self, id_activite, id_user, date_like):
        """Constructeur"""
        self.id_activite = id_activite
        self.id_user = id_user
        self.date_like = date_like
