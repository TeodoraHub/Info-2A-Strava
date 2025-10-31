class Commentaire:
    """
    Classe représentant un commentaire

    Attributs
    ----------
    id_comment : int
        identifiant du commentaire
    id_activite : int
        identifiant de l'activité
    contenu : str
        contenu du commentaire
    date_commentaire : Date
        date du commentaire
    id_user : int
        identifiant de l'utilisateur qui commente l'activité
    """

    def __init__(self, id_activite, contenu, date_commentaire, id_user, id_comment=None):
        """Constructeur"""
        self.id_comment = id_comment
        self.id_activite = id_activite
        self.contenu = contenu
        self.date_commentaire = date_commentaire
        self.id_user = id_user
