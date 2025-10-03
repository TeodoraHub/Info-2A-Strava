from datetime import date


class Like:
    """Classe pour gérer  les likes sur les activités"""

    def __init__(self, id_activite: int, id_user: int, date_like: date):
        self.id_activite = id_activite
        self.id_user = id_user
        self.date_like = date_like
