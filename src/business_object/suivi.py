from datetime import date


class Suivi:
    """Classe pour gérer les relations de suivi entre utilisateurs"""

    def __init__(self, id_user_suiveur: int, id_user_suivi: int, date_suivi: date):
        self.id_user_suiveur = id_user_suiveur
        self.id_user_suivi = id_user_suivi
        self.date_suivi = date_suivi
