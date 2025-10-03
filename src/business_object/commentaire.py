from datetime import date


class Commentaire:
    """Classe pour gérer les commentaires sur les activités"""

    def __init__(self, id_activite: int, contenu: str, date_commentaire: date, id_user: int):
        self.id_activite = id_activite
        self.contenu = contenu
        self.date_commentaire = date_commentaire
        self.id_user = id_user
